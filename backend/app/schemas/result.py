from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResultEvaluation(BaseModel):
    # Converts the SQLAlchemy Evaluation object into this schema.
    model_config = ConfigDict(from_attributes=True)

    correctness_score: float
    relevance_score: float
    completeness_score: float
    clarity_score: float
    overall_score: float

    strengths: str
    weaknesses: str
    improvement_feedback: str


class ResultAnswer(BaseModel):
    # Information about the submitted answer.
    answer_id: int
    question_id: int
    question_text: str | None
    answer_text: str

    # Evaluation may be missing in an inconsistent/partial result.
    evaluation: ResultEvaluation | None


class InterviewResultResponse(BaseModel):
    # Basic interview information.
    interview_id: int
    candidate_id: int
    candidate_name: str | None
    interview_type: str
    status: str

    # Progress information.
    total_questions: int
    answered_questions: int
    completion_percentage: float

    # Average of all evaluated answer scores.
    overall_score: float | None

    # Evaluation for every submitted answer.
    evaluations: list[ResultAnswer]

    # Interview timing.
    started_at: datetime | None
    completed_at: datetime | None
    duration_seconds: int | None
