from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)

    interview_type = Column(
        String(100),
        nullable=False,
    )

    category = Column(
        String(100),
        nullable=False,
    )

    question_text = Column(
        Text,
        nullable=False,
    )

    difficulty = Column(
        String(50),
        nullable=False,
    )

    question_order = Column(
        Integer,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
