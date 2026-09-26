from pydantic import BaseModel, Field


class ResumeResponse(BaseModel):
    candidate_id: int
    filename: str
    interview_type: str
    message: str
