import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.models.models import User, RecruiterProfile, CandidateProfile
from backend.models.enums import UserRole
from backend.schemas.schemas import RecruiterProfileCreate, CandidateProfileCreate, OnboardingStatusResponse
from backend.dependencies.auth_deps import get_current_user

logger = logging.getLogger("resume_screener")

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

@router.get("/status", response_model=OnboardingStatusResponse)
def get_onboarding_status(current_user: User = Depends(get_current_user)):
    """Returns the user's onboarding completion status and role."""
    return {
        "profile_completed": current_user.profile_completed,
        "role": current_user.role
    }

@router.post("/recruiter", status_code=status.HTTP_201_CREATED)
def create_recruiter_profile(
    profile_in: RecruiterProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Creates a recruiter profile and marks onboarding as completed."""
    logger.info("Recruiter onboarding submission for user: %s", current_user.email)
    
    if current_user.profile_completed:
        logger.warning("Onboarding rejected: User %s has already completed onboarding.", current_user.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding has already been completed."
        )

    # Check for existing profile in db just in case
    existing_profile = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == current_user.id).first()
    if existing_profile:
        current_user.profile_completed = True
        current_user.role = UserRole.RECRUITER
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding has already been completed."
        )

    # Create recruiter profile
    profile = RecruiterProfile(
        user_id=current_user.id,
        company_name=profile_in.company_name,
        company_type=profile_in.company_type,
        hiring_domain=profile_in.hiring_domain
    )
    db.add(profile)
    
    # Update user state
    current_user.profile_completed = True
    current_user.role = UserRole.RECRUITER
    
    db.commit()
    logger.info("Successfully completed recruiter onboarding for user: %s", current_user.email)
    return {"message": "Recruiter onboarding completed successfully."}

@router.post("/candidate", status_code=status.HTTP_201_CREATED)
def create_candidate_profile(
    profile_in: CandidateProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Creates a candidate profile and marks onboarding as completed."""
    logger.info("Candidate onboarding submission for user: %s", current_user.email)
    
    if current_user.profile_completed:
        logger.warning("Onboarding rejected: User %s has already completed onboarding.", current_user.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding has already been completed."
        )

    # Check for existing profile in db just in case
    existing_profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if existing_profile:
        current_user.profile_completed = True
        current_user.role = UserRole.CANDIDATE
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding has already been completed."
        )

    # Create candidate profile
    profile = CandidateProfile(
        user_id=current_user.id,
        current_status=profile_in.current_status,
        field_of_study=profile_in.field_of_study,
        current_domain=profile_in.current_domain
    )
    db.add(profile)
    
    # Update user state
    current_user.profile_completed = True
    current_user.role = UserRole.CANDIDATE
    
    db.commit()
    logger.info("Successfully completed candidate onboarding for user: %s", current_user.email)
    return {"message": "Candidate onboarding completed successfully."}
