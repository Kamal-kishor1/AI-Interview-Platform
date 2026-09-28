from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Evaluation(Base):

    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    # unique=True enforces 1:1 between Answer and Evaluation
    answer_id = Column(
        Integer,
        ForeignKey("answers.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    correctness_score = Column(Float, nullable=False)
    relevance_score = Column(Float, nullable=False)
    completeness_score = Column(Float, nullable=False)
    clarity_score = Column(Float, nullable=False)
    overall_score = Column(Float, nullable=False)

    strengths = Column(Text, nullable=False)
    weaknesses = Column(Text, nullable=False)
    improvement_feedback = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # optional relationship back to the answer model

    answer = relationship("Answer", back_populates="evaluation")
