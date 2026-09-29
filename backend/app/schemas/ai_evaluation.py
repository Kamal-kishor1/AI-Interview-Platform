from pydantic import BaseModel, Field


class AIEvaluationResponse(BaseModel):
    correctness_score: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="How technically correct the candidate's answer is, from 0 to 10.",
    )

    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="How directly the answer addresses the question, from 0 to 10.",
    )

    completeness_score: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="How completely the answer covers the important concepts, from 0 to 10.",
    )

    clarity_score: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="How clearly and understandably the answer is explained, from 0 to 10.",
    )

    strengths: str = Field(
        ...,
        min_length=1,
        description="The strongest aspects of the candidate's answer.",
    )

    weaknesses: str = Field(
        ...,
        min_length=1,
        description="The important weaknesses or missing aspects of the answer.",
    )

    improvement_feedback: str = Field(
        ...,
        min_length=1,
        description="Specific actionable advice for improving the answer.",
    )
