from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func

from app.core.database import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(
        Integer,
        primary_key=True,
    )

    interview_id = Column(
        Integer,
        ForeignKey(
            "interviews.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    question_id = Column(
        Integer,
        ForeignKey(
            "questions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    answer_text = Column(
        Text,
        nullable=False,
    )

    submitted_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
