from fastapi import APIRouter

router = APIRouter(prefix="/candidate", tags=["candidate"])

@router.get("/status")
def candidate_status():
    """Placeholder endpoint for future candidate-facing features."""
    return {"status": "candidate service is active"}
