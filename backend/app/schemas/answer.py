from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class AnswerCreate(BaseModel):
    question_id: int
    answer_text: str


class AnswerResponse(AnswerCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    interview_id: int
    question_id: int
    answer_text: str
    submitted_at: datetime


class AnswerSubmitResponse(BaseModel):
    answer_id: int
    interview_id: int
    question_id: int
    question_number: int
    total_questions: int
    answer_saved: bool
    interview_completed: bool
    next_question_id: int | None = None
    next_question_number: int | None = None
    next_question_text: str | None = None
