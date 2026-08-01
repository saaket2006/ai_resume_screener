import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.models.models import User, RecruiterProfile, CandidateProfile
from backend.models.enums import UserRole
from backend.schemas.schemas import OnboardingSubmission, OnboardingStatusResponse
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

@router.post("", status_code=status.HTTP_201_CREATED)
def submit_onboarding(
    submission: OnboardingSubmission,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Creates a user profile based on the role and marks onboarding as completed."""
    logger.info(f"Onboarding submission for user: {current_user.email} with role: {submission.role}")
    
    if current_user.profile_completed:
        logger.warning(f"Onboarding rejected: User {current_user.email} has already completed onboarding.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding has already been completed."
        )

    if submission.role == UserRole.RECRUITER:
        existing_profile = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == current_user.id).first()
        if existing_profile:
            current_user.profile_completed = True
            current_user.role = UserRole.RECRUITER
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Onboarding has already been completed."
            )

        profile = RecruiterProfile(
            user_id=current_user.id,
            company_name=submission.question_1,
            company_type=submission.question_2,
            hiring_domain=submission.question_3
        )
        db.add(profile)

    elif submission.role == UserRole.CANDIDATE:
        existing_profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
        if existing_profile:
            current_user.profile_completed = True
            current_user.role = UserRole.CANDIDATE
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Onboarding has already been completed."
            )

        profile = CandidateProfile(
            user_id=current_user.id,
            current_status=submission.question_1,
            field_of_study=submission.question_2,
            current_domain=submission.question_3
        )
        db.add(profile)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role specified."
        )

    current_user.profile_completed = True
    current_user.role = submission.role
    
    db.commit()
    logger.info(f"Successfully completed onboarding for user: {current_user.email}")
    return {"message": "Onboarding completed successfully."}
