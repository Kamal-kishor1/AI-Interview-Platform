from sqlalchemy import Column, Integer, String, DateTime, func, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Candidates(Base):

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    resume_filename = Column(String(255), nullable=True)
    resume_text = Column(Text, nullable=False)
    interview_type = Column(String(100), nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # relationship:
    interviews = relationship("Interview", back_populates="candidate")
