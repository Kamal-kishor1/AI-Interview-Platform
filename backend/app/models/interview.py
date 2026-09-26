from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from app.core.database import Base


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

    status = Column(
        String(50),
        nullable=False,
    )

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
