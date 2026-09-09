import logging
import datetime
from typing import Dict, Any, Optional

class AnalysisContext:
    """
    Lightweight, shared context carrying tracing IDs, configurations,
    and stage execution metrics across all pipeline stages.
    """
    def __init__(
        self,
        request_id: str,
        event: Any = None,
        analysis_id: Optional[int] = None,
        candidate_id: Optional[int] = None,
        recruiter_id: Optional[int] = None,
        profile_id: Optional[int] = None,
        configuration: Optional[Dict[str, Any]] = None
    ):
        self._request_id = request_id
        self._analysis_id = analysis_id
        self._candidate_id = candidate_id
        self._recruiter_id = recruiter_id
        self._profile_id = profile_id
        self._timestamps = {"created_at": datetime.datetime.utcnow().isoformat() + "Z"}
        self.event = event
        self.logger = logging.getLogger("resume_screener")
        self.configuration = configuration or {}
        self.metrics = {}  # {stage_name: {start_time, end_time, duration_ms, status}}

    @property
    def request_id(self) -> str:
        return self._request_id

    @property
    def analysis_id(self) -> Optional[int]:
        return self._analysis_id

    @property
    def candidate_id(self) -> Optional[int]:
        return self._candidate_id

    @property
    def recruiter_id(self) -> Optional[int]:
        return self._recruiter_id

    @property
    def profile_id(self) -> Optional[int]:
        return self._profile_id

    @property
    def timestamps(self) -> Dict[str, str]:
        return self._timestamps
