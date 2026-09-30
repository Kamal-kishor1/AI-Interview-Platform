from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, model_validator


class DifficultyLevel(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class InterviewCreate(BaseModel):
    candidate_id: int

    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    question_count: int = Field(default=10, ge=5, le=30)

    use_skills: bool = True
    use_projects: bool = True
    use_experience: bool = True
    use_resume: bool = True

    @model_validator(mode="after")
    def validate_personalization(self):
        if not any(
            [self.use_skills, self.use_projects, self.use_experience, self.use_resume]
        ):

            raise ValueError("At least one personalization source must be selected.")

        return self


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
