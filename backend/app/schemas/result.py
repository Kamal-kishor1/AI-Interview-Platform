from pydantic import BaseModel
from datetime import datetime


class InterviewResultResponse(BaseModel):
    interview_id: int
    candidate_id: int
    candidate_name: str
    interview_type: str
    status: str

    total_questions: int
    answered_questions: int
    completion_percentage: float

    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_seconds: int | None = None
