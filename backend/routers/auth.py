from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import logging
import urllib.request
import json
import jwt as pyjwt
from pydantic import BaseModel

from backend.database.database import get_db
from backend.models.models import User
from backend.models.enums import UserRole
from backend.schemas.schemas import UserCreate, UserLogin, Token, UserResponse
from backend.dependencies.auth_utils import get_password_hash, verify_password, create_access_token
from backend.dependencies.auth_deps import get_current_user
from backend.config import settings

logger = logging.getLogger("resume_screener")

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user inside the database with profile_completed = False and UserRole.UNASSIGNED."""
    logger.info("Sign up attempt for email: %s", user_in.email)
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        logger.warning("Sign up failed: email %s already registered", user_in.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_pwd = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed_pwd,
        role=user_in.role or UserRole.UNASSIGNED,
        profile_completed=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("Successfully registered user: %s with profile_completed: False and role: %s", user.email, user.role)
    return user

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticates a user and issues a JWT token containing email and role."""
    logger.info("Login attempt for email: %s", credentials.email)
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        logger.warning("Login failed: invalid credentials for email %s", credentials.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate token (role can be None/UNASSIGNED if profile not completed)
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRY_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value if user.role else None},
        expires_delta=access_token_expires
    )
    logger.info("Successfully authenticated user %s. Issuing token...", user.email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Retrieves the authenticated user's profile details."""
    return current_user

# Helper schema for Google Login
class GoogleLoginRequest(BaseModel):
    id_token: str

# Cache for Google JWKs public certs
_certs_cache = {}
_certs_expiry = 0

def fetch_google_certs():
    global _certs_cache, _certs_expiry
    import time
    now = time.time()
    if not _certs_cache or now > _certs_expiry:
        try:
            with urllib.request.urlopen("https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com", timeout=5) as response:
                _certs_cache = json.loads(response.read().decode("utf-8"))
                _certs_expiry = now + 3600  # Cache for 1 hour
        except Exception as e:
            logger.error("Failed to fetch Google certificates: %s", e)
            if not _certs_cache:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Failed to retrieve Google authentication certificates"
                )
    return _certs_cache

def verify_firebase_token(id_token: str) -> dict:
    try:
        header = pyjwt.get_unverified_header(id_token)
        kid = header.get("kid")
        if not kid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token missing kid header")
            
        certs = fetch_google_certs()
        cert_pem = certs.get(kid)
        if not cert_pem:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token kid")
            
        from cryptography.x509 import load_pem_x509_certificate
        try:
            cert_obj = load_pem_x509_certificate(cert_pem.encode())
            public_key = cert_obj.public_key()
        except Exception as e:
            logger.error("Failed to parse X509 certificate: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to load public key from Google certificate"
            )
            
        project_id = settings.FIREBASE_PROJECT_ID
        payload = pyjwt.decode(
            id_token,
            public_key,
            algorithms=["RS256"],
            audience=project_id,
            issuer=f"https://securetoken.google.com/{project_id}",
            leeway=120
        )
        return payload
    except pyjwt.ExpiredSignatureError as e:
        logger.error("Firebase token signature expired: %s", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google token has expired")
    except pyjwt.InvalidTokenError as e:
        logger.error("Firebase token validation failed: %s", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Google token: {str(e)}")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Unexpected token verification error: %s", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Token verification failed: {str(e)}")

@router.post("/google", response_model=Token)
def google_login(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    """Verifies Firebase Google ID Token and issues a local backend JWT token."""
    logger.info("Google/Firebase login attempt")
    try:
        google_user = verify_firebase_token(payload.id_token)
        email = google_user.get("email")
        if not email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google token missing email claim")
            
        # Check if user exists, else register
        user = db.query(User).filter(User.email == email).first()
        if not user:
            logger.info("Registering new user via Google Sign-In: %s", email)
            user = User(
                email=email,
                hashed_password="",  # Empty password since authenticated via Google
                role=UserRole.UNASSIGNED,
                profile_completed=False
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            logger.info("User logged in via Google: %s", email)
            
        # Generate token
        access_token_expires = timedelta(minutes=settings.JWT_EXPIRY_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role.value if user.role else None},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Google auth handler failed: %s", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
