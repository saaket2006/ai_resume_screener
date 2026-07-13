"""
Event-Based/Stage-Based Analysis Pipeline for AI Resume Screener.
Defines clean data contracts (payloads/events) and sequential stages
to handle Resume Text Extraction, Skill Extraction, Semantic Matching,
Scoring, Explanation Building (XAI), and Database Persistence.
"""

import time
import logging
import datetime
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from backend.config import settings
from backend.services.nlp_service import preprocess_text
from backend.services.skill_extractor import extract_skills
from backend.services.document_service import extract_text
from backend.services.info_extractor import (
    extract_name, extract_email, extract_phone, extract_linkedin,
    extract_github, extract_experience, extract_relevant_internships,
    extract_education, extract_projects
)
from backend.services.semantic.matcher import SemanticMatcher
from backend.services.semantic.scorer import SemanticScorer
from backend.services.metadata_builder import build_analysis_metadata
from backend.models.models import Resume, ScanResult
from backend.models.enums import ResumeStatus

logger = logging.getLogger("resume_screener")

# ==========================================
# 1. Pipeline Event / Payload Contracts
# ==========================================

class PipelineEvent:
    """Base class for all pipeline stages' input/output data contracts."""
    pass

class ResumeExtractedEvent(PipelineEvent):
    def __init__(self, filename: str, content_bytes: bytes, job_description: str, clean_jd: str):
        self.filename = filename
        self.content_bytes = content_bytes
        self.job_description = job_description
        self.clean_jd = clean_jd
        
        self.raw_text = ""
        self.clean_text = ""
        self.file_ext = filename.split(".")[-1].lower() if "." in filename else "unknown"
        
        self.status = "success"  # "success" or "error"
        self.error_message = ""

class SkillsExtractedEvent(PipelineEvent):
    def __init__(self, extraction: ResumeExtractedEvent):
        self.extraction = extraction
        self.jd_skills_objs: List[Any] = []
        self.jd_skills_names: List[str] = []
        self.candidate_skills_objs: List[Any] = []
        
        # Copy status from previous event
        self.status = extraction.status
        self.error_message = extraction.error_message

class SemanticMatchedEvent(PipelineEvent):
    def __init__(self, skills: SkillsExtractedEvent):
        self.skills = skills
        self.match_results: List[Any] = []
        self.matched_serialized: List[str] = []
        self.missing_serialized: List[str] = []
        self.semantic_metadata_payload: Dict[str, Any] = {}
        
        self.status = skills.status
        self.error_message = skills.error_message

class ScoredEvent(PipelineEvent):
    def __init__(self, matching: SemanticMatchedEvent):
        self.matching = matching
        self.semantic_score = 0.0
        
        # Candidate Info
        self.candidate_name = "N/A"
        self.candidate_email = "N/A"
        self.candidate_phone = "N/A"
        self.candidate_linkedin = "Not Provided"
        self.candidate_github = "Not Provided"
        self.candidate_experience = 0
        self.candidate_internships = 0
        self.candidate_education = "None"
        self.candidate_projects = 0
        
        # Individual scores (calculated or placeholder)
        self.similarity_score = 0.0
        self.skill_score = 0.0
        self.experience_score = 0.0
        self.education_score = 0.0
        self.projects_score = 0.0
        self.doc_similarity_score = 0.0
        
        self.status = matching.status
        self.error_message = matching.error_message

class ExplanationBuiltEvent(PipelineEvent):
    def __init__(self, scoring: ScoredEvent):
        self.scoring = scoring
        self.analysis_metadata: Dict[str, Any] = {}
        self.xai_explanations: Dict[str, str] = {}
        
        self.status = scoring.status
        self.error_message = scoring.error_message

class PersistenceEvent(PipelineEvent):
    def __init__(self, explanation: ExplanationBuiltEvent):
        self.explanation = explanation
        self.resume_id: Optional[int] = None
        self.scan_result_id: Optional[int] = None
        
        self.status = explanation.status
        self.error_message = explanation.error_message


# ==========================================
# 2. Pipeline Abstract / Concrete Stages
# ==========================================

class PipelineStage(ABC):
    """Abstract base class representing a single pipeline stage."""
    
    @abstractmethod
    def execute(self, event: Any) -> Any:
        pass


class ResumeTextExtractionStage(PipelineStage):
    """Stage 1: Validates and extracts raw text from resume bytes."""
    
    def execute(self, event: ResumeExtractedEvent) -> ResumeExtractedEvent:
        if event.status != "success":
            return event
            
        # File type validation
        if not any(event.filename.lower().endswith(ext) for ext in settings.ALLOWED_EXTENSIONS):
            logger.warning("Skipping '%s': Unsupported file extension", event.filename)
            event.status = "error"
            event.error_message = "Unsupported/Invalid File"
            return event
            
        # File size validation
        if len(event.content_bytes) > settings.MAX_FILE_SIZE:
            logger.warning("Skipping '%s': File size (%d bytes) exceeds limit (%d bytes)", 
                           event.filename, len(event.content_bytes), settings.MAX_FILE_SIZE)
            event.status = "error"
            event.error_message = "File Too Large (>5MB)"
            return event
            
        # Text extraction
        try:
            event.raw_text = extract_text(event.content_bytes, event.filename)
            event.clean_text = preprocess_text(event.raw_text)
        except Exception as e:
            logger.error("Skipping '%s': Text extraction failed: %s", event.filename, e)
            event.status = "error"
            event.error_message = "Unreadable File"
            
        return event


class SkillExtractionStage(PipelineStage):
    """Stage 2: Extracts technical skills from raw text."""
    
    def execute(self, event: ResumeExtractedEvent) -> SkillsExtractedEvent:
        output = SkillsExtractedEvent(event)
        if output.status != "success":
            return output
            
        try:
            # Extract skills from job description and candidate resume
            output.jd_skills_objs = extract_skills(event.job_description)
            output.jd_skills_names = [s.canonical_name.lower() for s in output.jd_skills_objs]
            output.candidate_skills_objs = extract_skills(event.raw_text)
        except Exception as e:
            logger.error("Skill extraction stage failed: %s", e)
            output.status = "error"
            output.error_message = "Skill extraction failed"
            
        return output


class SemanticMatchingStage(PipelineStage):
    """Stage 3: Performs semantic skill matching using the Semantic Scoring Engine."""
    
    def execute(self, event: SkillsExtractedEvent) -> SemanticMatchedEvent:
        output = SemanticMatchedEvent(event)
        if output.status != "success":
            return output
            
        try:
            matcher = SemanticMatcher()
            scorer = SemanticScorer()
            
            match_results = matcher.match_skills(event.jd_skills_objs, event.candidate_skills_objs)
            semantic_breakdown = scorer.calculate_score(match_results)
            semantic_score = semantic_breakdown["overall"]
            
            output.match_results = match_results
            
            # Serialize for backward compatibility
            output.matched_serialized = sorted(list(set([
                res.required_skill.canonical_name.lower()
                for res in match_results
                if res.match_type != "UNKNOWN"
            ])))
            output.missing_serialized = sorted(list(set([
                res.required_skill.canonical_name.lower()
                for res in match_results
                if res.match_type == "UNKNOWN"
            ])))
            
            # Construct semantic metadata payload
            exact_list = []
            alias_list = []
            hierarchical_list = []
            family_list = []
            
            for res in match_results:
                item = {
                    "required": res.required_skill.canonical_name,
                    "candidate": res.candidate_skill.canonical_name,
                    "confidence": res.confidence,
                    "weight": res.weight,
                    "reason": res.reason
                }
                if res.match_type == "EXACT":
                    exact_list.append(item)
                elif res.match_type in ("ALIAS", "ABBREVIATION"):
                    alias_list.append(item)
                elif res.match_type == "HIERARCHICAL":
                    hierarchical_list.append(item)
                elif res.match_type == "TECHNOLOGY_FAMILY":
                    family_list.append(item)
                    
            output.semantic_metadata_payload = {
                "exact_matches": exact_list,
                "alias_matches": alias_list,
                "hierarchical_matches": hierarchical_list,
                "family_matches": family_list,
                "semantic_score": semantic_score
            }
        except Exception as e:
            logger.error("Semantic matching stage failed: %s", e)
            output.status = "error"
            output.error_message = "Semantic matching failed"
            
        return output


class ScoringStage(PipelineStage):
    """Stage 4: Scores candidate details (experience, education, projects, document similarity)."""
    
    def execute(self, event: SemanticMatchedEvent) -> ScoredEvent:
        output = ScoredEvent(event)
        if output.status != "success":
            return output
            
        try:
            raw_text = event.skills.extraction.raw_text
            jd_skills = event.skills.jd_skills_names
            
            # Extract candidate metadata details
            output.candidate_name = extract_name(raw_text)
            output.candidate_email = extract_email(raw_text)
            output.candidate_phone = extract_phone(raw_text)
            output.candidate_linkedin = extract_linkedin(raw_text)
            output.candidate_github = extract_github(raw_text)
            output.candidate_experience = extract_experience(raw_text)
            output.candidate_internships = extract_relevant_internships(raw_text, jd_skills)
            output.candidate_education = extract_education(raw_text)
            output.candidate_projects = extract_projects(raw_text)
            
            # Pull scores from matching event
            output.semantic_score = event.semantic_metadata_payload.get("semantic_score", 0.0)
            output.skill_score = output.semantic_score
            
            # 1. Experience Score (Max 10 years for 100%)
            effective_exp_years = output.candidate_experience + (output.candidate_internships * 0.5)
            output.experience_score = min((effective_exp_years / 10.0) * 100, 100)
            
            # 2. Education Score
            education = output.candidate_education
            if education == "PhD":
                output.education_score = 100
            elif education == "Master":
                output.education_score = 80
            elif education == "Bachelor":
                output.education_score = 60
            else:
                output.education_score = 20
                
            # 3. Projects Score
            output.projects_score = (output.candidate_projects / 5.0) * 100
            
            # 4. Overall Similarity Score
            output.similarity_score = (output.skill_score * 0.50) + (output.experience_score * 0.25) + (output.education_score * 0.15) + (output.projects_score * 0.10)
            output.similarity_score = round(output.similarity_score, 2)
            
            # 5. TF-IDF Cosine Similarity for Document Similarity Component
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                from sklearn.metrics.pairwise import cosine_similarity
                
                jd_text = " ".join(jd_skills)
                cand_text = " ".join(event.matched_serialized)
                
                if jd_text.strip() and cand_text.strip():
                    vectorizer = TfidfVectorizer(stop_words='english')
                    tfidf_jd = vectorizer.fit_transform([jd_text])
                    if len(vectorizer.vocabulary_) > 0:
                        tfidf_cand = vectorizer.transform([cand_text])
                        sim = float(cosine_similarity(tfidf_jd, tfidf_cand).flatten()[0]) * 100
                        output.doc_similarity_score = round(sim, 2)
                    else:
                        output.doc_similarity_score = 0.0
                else:
                    output.doc_similarity_score = 0.0
            except Exception as ex:
                logger.error("Failed to compute TF-IDF similarity in stage: %s", ex)
                output.doc_similarity_score = 0.0
                
        except Exception as e:
            logger.error("Scoring stage failed: %s", e)
            output.status = "error"
            output.error_message = "Scoring failed"
            
        return output


class ExplanationBuildingStage(PipelineStage):
    """Stage 5: Builds structured score explanations (XAI)."""
    
    def execute(self, event: ScoredEvent) -> ExplanationBuiltEvent:
        output = ExplanationBuiltEvent(event)
        if output.status != "success":
            return output
            
        try:
            from backend.services.xai.builder import build_score_components
            from backend.services.xai.engine import XaiEngine
            
            # 1. Build score components list with Evidence items
            components = build_score_components(
                scoring_event=event,
                match_results=event.matching.match_results,
                doc_similarity_percentage=event.doc_similarity_score
            )
            
            # 2. Compile multi-level explanations
            xai_engine = XaiEngine()
            explanations = xai_engine.generate_explanations(components)
            
            # 3. Overall Summary reasoning
            overall_reason = explanations.get("overall", {}).get("summary", {}).get("why_awarded", "Overall score computed successfully.")
            
            # 4. Serialize components for Pydantic version-safe storage
            serialized_comps = []
            for comp in components:
                ev_list = []
                for ev in comp.evidence:
                    ev_list.append({
                        "type": ev.type,
                        "category": ev.category,
                        "title": ev.title,
                        "description": ev.description,
                        "importance": ev.importance,
                        "related_skill": ev.related_skill,
                        "confidence": ev.confidence
                    })
                serialized_comps.append({
                    "name": comp.name,
                    "raw_score": comp.raw_score,
                    "weight": comp.weight,
                    "weighted_score": comp.weighted_score,
                    "max_score": comp.max_score,
                    "status": comp.status,
                    "details": comp.details,
                    "evidence": ev_list
                })
            
            # Construct candidate result map for standard metadata builder
            cand_dict = {
                "name": event.candidate_name,
                "email": event.candidate_email,
                "phone": event.candidate_phone,
                "linkedin": event.candidate_linkedin,
                "github": event.candidate_github,
                "experience": event.candidate_experience,
                "education": event.candidate_education,
                "projects": event.candidate_projects,
                "similarity_score": event.similarity_score,
                "skill_score": event.skill_score,
                "experience_score": event.experience_score,
                "education_score": event.education_score,
                "projects_score": event.projects_score,
                "matched_skills": event.matching.matched_serialized,
                "missing_skills": event.matching.missing_serialized
            }
            
            # Generate base analysis_metadata schema
            output.analysis_metadata = build_analysis_metadata(
                candidate_result=cand_dict,
                processing_time_ms=0,
                parser=event.matching.skills.extraction.file_ext,
                document_type=event.matching.skills.extraction.file_ext,
                semantic_data=event.matching.semantic_metadata_payload
            )
            
            # Enrich with complete structured XAI block
            output.analysis_metadata["xai"] = {
                "enabled": True,
                "components": serialized_comps,
                "overall_summary": overall_reason,
                "explanations": explanations
            }
            
            # Set flat fields for legacy compatibility / logs
            output.xai_explanations = {
                "skills_summary": explanations.get("skills", {}).get("summary", {}).get("why_awarded", ""),
                "experience_summary": explanations.get("experience", {}).get("summary", {}).get("why_awarded", ""),
                "education_summary": explanations.get("education", {}).get("summary", {}).get("why_awarded", ""),
                "projects_summary": explanations.get("projects", {}).get("summary", {}).get("why_awarded", ""),
                "overall_reasoning": overall_reason
            }
            
        except Exception as e:
            logger.error("Explanation building stage failed: %s", e)
            output.status = "error"
            output.error_message = "Explanation building failed"
            
        return output


class PersistenceStage(PipelineStage):
    """Stage 6: Persists Resume and ScanResult to the database transactionally."""
    
    def __init__(self, db: Session):
        self.db = db
        
    def execute(self, event: ExplanationBuiltEvent, **kwargs) -> PersistenceEvent:
        output = PersistenceEvent(event)
        if output.status != "success":
            return output
            
        try:
            # Extract arguments
            candidate_id = kwargs.get("candidate_id")
            version = kwargs.get("version", 1)
            label = kwargs.get("label")
            label_source = kwargs.get("label_source", "SYSTEM")
            job_description_id = kwargs.get("job_description_id")
            ats_score = kwargs.get("ats_score", 0.0)
            elapsed_ms = kwargs.get("elapsed_ms", 0)
            
            scoring = event.scoring
            extraction = scoring.matching.skills.extraction
            
            # Build final analysis_metadata with correct overall ats_score and elapsed time
            meta = event.analysis_metadata
            meta["score"]["overall"] = ats_score
            meta["engine"]["processing_time_ms"] = elapsed_ms
            
            # Save Resume model
            resume = Resume(
                candidate_id=candidate_id,
                extracted_text=extraction.raw_text,
                original_filename=extraction.filename,
                file_type=extraction.file_ext,
                version=version,
                label=label,
                label_source=label_source,
                status=ResumeStatus.ACTIVE
            )
            self.db.add(resume)
            self.db.flush()  # get resume.id
            
            # Save ScanResult model
            scan_result = ScanResult(
                resume_id=resume.id,
                job_description_id=job_description_id,
                ats_score=ats_score,
                analysis_metadata=meta
            )
            self.db.add(scan_result)
            self.db.flush()
            
            output.resume_id = resume.id
            output.scan_result_id = scan_result.id
            
            # Sync back to output.explanation.scoring
            output.explanation.scoring.similarity_score = ats_score
            
            logger.info("Pipeline persisted Resume ID %d and ScanResult ID %d successfully", resume.id, scan_result.id)
        except Exception as e:
            self.db.rollback()
            logger.error("Persistence stage failed: %s", e)
            output.status = "error"
            output.error_message = f"Database persistence failed: {str(e)}"
            
        return output


# ==========================================
# 3. Pipeline Runner / Orchestrator
# ==========================================

class AnalysisPipeline:
    """Orchestrator to run raw resume payloads through sequential pipeline stages."""
    
    def __init__(self):
        self.extraction_stage = ResumeTextExtractionStage()
        self.skills_stage = SkillExtractionStage()
        self.semantic_stage = SemanticMatchingStage()
        self.scoring_stage = ScoringStage()
        self.explanation_stage = ExplanationBuildingStage()

    def run_analysis(self, filename: str, content_bytes: bytes, job_description: str, clean_jd: str) -> ExplanationBuiltEvent:
        """Runs stages 1 through 5 of the analysis pipeline."""
        # Stage 1: Extraction
        extraction_event = ResumeExtractedEvent(
            filename=filename,
            content_bytes=content_bytes,
            job_description=job_description,
            clean_jd=clean_jd
        )
        extraction_result = self.extraction_stage.execute(extraction_event)
        
        # Stage 2: Skill Extraction
        skills_result = self.skills_stage.execute(extraction_result)
        
        # Stage 3: Semantic Matching
        matching_result = self.semantic_stage.execute(skills_result)
        
        # Stage 4: Scoring
        scoring_result = self.scoring_stage.execute(matching_result)
        
        # Stage 5: Explanation Building
        explanation_result = self.explanation_stage.execute(scoring_result)
        
        return explanation_result
