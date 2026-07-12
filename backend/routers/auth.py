from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

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
