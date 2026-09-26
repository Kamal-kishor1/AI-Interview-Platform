from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class CandidateCreate(BaseModel):
    name: str
    email: str


class CandidateResponse(CandidateCreate):
    id: int
    resume_filename: str
    interview_type: str | None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)
