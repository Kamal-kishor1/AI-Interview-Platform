from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EvaluationBase(BaseModel):
    correctness_score: float = Field(..., ge=0.0, le=10.0)
    relevance_score: float = Field(..., ge=0.0, le=10.0)
    completeness_score: float = Field(..., ge=0.0, le=10.0)
    clarity_score: float = Field(..., ge=0.0, le=10.0)

    strengths: str = Field(..., min_length=1)
    weaknesses: str = Field(..., min_length=1)
    improvement_feedback: str = Field(..., min_length=1)


class EvaluationCreate(EvaluationBase):
    answer_id: int


class EvaluationResponse(EvaluationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    answer_id: int
    overall_score: float
    created_at: datetime
