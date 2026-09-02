
import time
import datetime
from typing import Optional
from sqlalchemy.orm import Session

from backend.services.pipeline.context import AnalysisContext
from backend.services.pipeline.events import ResumeExtractedEvent, RecommendationBuiltEvent
from backend.services.pipeline.stages import (
    PipelineStage, ResumeTextExtractionStage, SkillExtractionStage,
    SemanticMatchingStage, ScoringProfileResolutionStage, ScoringStage,
    ExplanationBuildingStage, RecommendationBuildingStage
)

class AnalysisPipeline:
    """Orchestrator to run raw resume payloads through sequential pipeline stages."""

    def __init__(self):
        self.extraction_stage = ResumeTextExtractionStage()
        self.skills_stage = SkillExtractionStage()
        self.semantic_stage = SemanticMatchingStage()
        self.profile_stage = ScoringProfileResolutionStage()
        self.scoring_stage = ScoringStage()
        self.explanation_stage = ExplanationBuildingStage()
        self.recommendation_stage = RecommendationBuildingStage()

    async def run_stage_with_metrics(self, stage: PipelineStage, context: AnalysisContext) -> AnalysisContext:
        stage_name = stage.__class__.__name__
        start_time = time.time()
        start_dt = datetime.datetime.utcnow().isoformat() + "Z"
        status = "success"
        try:
            import inspect
            if inspect.iscoroutinefunction(stage.execute):
                context = await stage.execute(context)
            else:
                context = stage.execute(context)
            if hasattr(context.event, "status") and context.event.status != "success":
                status = "error"
        except Exception as e:
            status = "error"
            context.logger.error(f"Stage {stage_name} failed: {e}")
            raise e
        finally:
            end_time = time.time()
            end_dt = datetime.datetime.utcnow().isoformat() + "Z"
            duration_ms = int((end_time - start_time) * 1000)
            context.metrics[stage_name] = {
                "start_time": start_dt,
                "end_time": end_dt,
                "duration_ms": duration_ms,
                "status": status
            }
        return context
    async def run_analysis(
        self,
        filename: str,
        content_bytes: bytes,
        job_description: str,
        clean_jd: str,
        db: Optional[Session] = None,
        context: Optional[AnalysisContext] = None
    ) -> RecommendationBuiltEvent:
        """Runs stages 1 through 7 of the analysis pipeline."""
        if context is None:
            import uuid
            context = AnalysisContext(request_id=str(uuid.uuid4()))

        # Configure db session on profile resolution stage
        self.profile_stage.db = db

        # Stage 1: Extraction
        context.event = ResumeExtractedEvent(
            filename=filename,
            content_bytes=content_bytes,
            job_description=job_description,
            clean_jd=clean_jd
        )
        context = await self.run_stage_with_metrics(self.extraction_stage, context)

        # Stage 2: Skill Extraction
        context = await self.run_stage_with_metrics(self.skills_stage, context)

        # Stage 3: Semantic Matching
        context = await self.run_stage_with_metrics(self.semantic_stage, context)

        # Stage 4: Scoring Profile Resolution
        context = await self.run_stage_with_metrics(self.profile_stage, context)
