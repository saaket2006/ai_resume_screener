from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from backend.models.enums import UserRole, CompanyType

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Optional[UserRole] = Field(default=None)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: Optional[UserRole] = None
    profile_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class RecruiterProfileResponse(BaseModel):
    id: int
    company_name: str
    company_type: CompanyType
    hiring_domain: str
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class CandidateProfileResponse(BaseModel):
    id: int
    current_status: str
    field_of_study: str
    current_domain: str
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    role: Optional[UserRole] = None
    profile_completed: bool
    created_at: datetime
    recruiter_profile: Optional[RecruiterProfileResponse] = None
    candidate_profile: Optional[CandidateProfileResponse] = None

    class Config:
        from_attributes = True
        orm_mode = True

class OnboardingStatusResponse(BaseModel):
    profile_completed: bool
    role: Optional[UserRole] = None

class OnboardingSubmission(BaseModel):
    role: UserRole
    question_1: str = Field(..., min_length=1)
    question_2: str = Field(..., min_length=1)
    question_3: str = Field(..., min_length=1)
