import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt as pyjwt
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.config import settings
from backend.models.models import User
from backend.models.enums import UserRole

logger = logging.getLogger("resume_screener")

# Declare OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Validates the JWT token and returns the corresponding User.
    Raises 401 Unauthorized if the token is invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = pyjwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except pyjwt.PyJWTError as e:
        logger.warning("JWT token decode failed: %s", e)
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.warning("User specified in JWT token does not exist: %s", email)
        raise credentials_exception
    return user

def require_recruiter(current_user: User = Depends(get_current_user)) -> User:
    """Restricts route access to users registered with the RECRUITER role."""
    if current_user.role != UserRole.RECRUITER:
        logger.warning("Access denied: User %s does not have RECRUITER role (role: %s)", current_user.email, current_user.role)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Recruiter access required"
        )
    return current_user

def require_candidate(current_user: User = Depends(get_current_user)) -> User:
    """Restricts route access to users registered with the CANDIDATE role."""
    if current_user.role != UserRole.CANDIDATE:
        logger.warning("Access denied: User %s does not have CANDIDATE role (role: %s)", current_user.email, current_user.role)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Candidate access required"
        )
    return current_user
