import logging
from sqlalchemy.orm import Session
from backend.models.models import ScoringProfile

logger = logging.getLogger("resume_screener")

DEFAULT_PROFILES = [
    {
        "name": "General Software Engineer",
        "description": "Balanced scoring profile suitable for general software engineering positions.",
        "target_role": "Software Engineer",
        "experience_level": "Mid",
        "domain": "Software Development",
        "weights": {"skills": 0.50, "experience": 0.25, "education": 0.15, "projects": 0.10},
        "is_default": True
    },
    {
        "name": "Backend Developer",
        "description": "Scoring profile biased towards language/architecture skills and solid experience.",
        "target_role": "Backend Engineer",
        "experience_level": "Mid-Senior",
        "domain": "Backend Development",
        "weights": {"skills": 0.45, "experience": 0.30, "education": 0.10, "projects": 0.15},
        "is_default": False
    },
    {
        "name": "Frontend Developer",
        "description": "Scoring profile prioritizing project counts, UI design and core front-end skills.",
        "target_role": "Frontend Engineer",
        "experience_level": "Mid",
        "domain": "Frontend Development",
        "weights": {"skills": 0.40, "experience": 0.20, "education": 0.10, "projects": 0.30},
        "is_default": False
    },
    {
        "name": "AI Engineer",
        "description": "Scoring profile emphasizing core AI/ML skills and high academic standards.",
        "target_role": "AI/ML Engineer",
        "experience_level": "Mid-Senior",
        "domain": "Artificial Intelligence",
        "weights": {"skills": 0.50, "experience": 0.20, "education": 0.20, "projects": 0.10},
        "is_default": False
    },
    {
        "name": "Data Scientist",
        "description": "Scoring profile strongly weighing academic degrees and analytical tool expertise.",
        "target_role": "Data Scientist",
        "experience_level": "Mid",
        "domain": "Data Science",
        "weights": {"skills": 0.40, "experience": 0.20, "education": 0.30, "projects": 0.10},
        "is_default": False
    },
    {
        "name": "DevOps Engineer",
        "description": "Scoring profile highlighting deployment projects and cloud infrastructure experience.",
        "target_role": "DevOps Engineer",
        "experience_level": "Senior",
        "domain": "DevOps / Infrastructure",
        "weights": {"skills": 0.45, "experience": 0.30, "education": 0.05, "projects": 0.20},
        "is_default": False
    },
    {
        "name": "Cybersecurity Engineer",
        "description": "Scoring profile placing heavy focus on professional tenure and security tools skills.",
        "target_role": "Cybersecurity Specialist",
        "experience_level": "Senior",
        "domain": "Information Security",
        "weights": {"skills": 0.45, "experience": 0.35, "education": 0.10, "projects": 0.10},
        "is_default": False
    },
    {
        "name": "Fresh Graduate",
        "description": "Scoring profile adjusted for low experience by focusing on education background and academic projects.",
        "target_role": "Junior Software Engineer",
        "experience_level": "Entry",
        "domain": "General Software Development",
        "weights": {"skills": 0.30, "experience": 0.10, "education": 0.30, "projects": 0.30},
        "is_default": False
    }
]

def seed_default_profiles(db: Session):
    """
    Checks if scoring profiles exist in the database; if not, seeds the default profiles.
    """
    try:
        count = db.query(ScoringProfile).count()
        if count == 0:
            logger.info("Seeding default scoring profiles...")
            for prof in DEFAULT_PROFILES:
                profile = ScoringProfile(
                    name=prof["name"],
                    description=prof["description"],
                    target_role=prof["target_role"],
                    experience_level=prof["experience_level"],
                    domain=prof["domain"],
                    weights=prof["weights"],
                    is_default=prof["is_default"]
                )
                db.add(profile)
            db.commit()
            logger.info("Successfully seeded default scoring profiles.")
        else:
            logger.debug("Scoring profiles already exist (%d found). Skipping seeding.", count)
    except Exception as e:
        db.rollback()
        logger.error("Failed to seed default scoring profiles: %s", e)
