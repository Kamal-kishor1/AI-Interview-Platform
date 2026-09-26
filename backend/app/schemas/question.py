from pydantic import BaseModel, Field


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    difficulty: str
    order: str
