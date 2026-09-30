from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, func
from enum import Enum
from sqlalchemy.orm import relationship

from app.core.database import Base


class DifficultyLevel(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(
        Integer,
        primary_key=True,
    )

    candidate_id = Column(
        Integer,
        ForeignKey(
            "candidates.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    interview_type = Column(
        String(100),
        nullable=False,
    )

    status = Column(String(50), nullable=False, default="PENDING")

    # New configuration columns

    difficulty = Column(
        String(10),
        nullable=False,
        default=DifficultyLevel.MEDIUM.value,
        server_default=DifficultyLevel.MEDIUM.value,
    )

    question_count = Column(Integer, nullable=False, default=10, server_default="10")

    use_skills = Column(Boolean, nullable=False, default=True, server_default="true")

    use_projects = Column(Boolean, nullable=False, default=True, server_default="true")

    use_experience = Column(
        Boolean, nullable=False, default=True, server_default="true"
    )

    use_resume = Column(Boolean, nullable=False, default=True, server_default="true")

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    candidate = relationship("Candidates", back_populates="interviews")
