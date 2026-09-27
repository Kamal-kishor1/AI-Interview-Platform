from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InterviewCreate(BaseModel):
    candidate_id: int


class InterviewResponse(InterviewCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    interview_type: str
    status: str
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None


class InterviewQuestionResponse(BaseModel):
    interview_id: int
    interview_type: str
    question_id: int
    question_number: int
    total_questions: int
    question_text: str
