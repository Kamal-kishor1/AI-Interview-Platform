from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.candidate import Candidates

# from app.schemas.candidate import CandidateCreate

# ---------------------------------------------------------
# Service Exceptions
# ---------------------------------------------------------


class CandidateServiceError(Exception):
    """Base exception for candidate service errors."""


class CandidateNotFoundError(CandidateServiceError):
    """Raised when a candidate does not exist."""


class CandidateCreationError(CandidateServiceError):
    """Raised when a candidate cannot be created."""


class CandidateUpdateError(CandidateServiceError):
    """Raised when a candidate cannot be updated."""


# ---------------------------------------------------------
# Candidate Service
# ---------------------------------------------------------


class CandidateService:

    # -----------------------------------------------------
    # Create Candidate
    # -----------------------------------------------------

    @staticmethod
    def create_candidate(
        db: Session,
        name: str,
        email: str,
        resume_filename: str,
        resume_text: str,
        interview_type: str,
    ) -> Candidates:

        clean_name = name.strip()
        clean_email = email.strip().lower()
        clean_resume_filename = resume_filename.strip()
        clean_resume_text = resume_text.strip()
        clean_interview_type = interview_type.strip()

        if not clean_name:
            raise CandidateCreationError("Candidate name cannot be empty.")

        if not clean_email:
            raise CandidateCreationError("Candidate email cannot be empty.")

        if not clean_resume_filename:
            raise CandidateCreationError("Resume filename cannot be empty.")

        if not clean_resume_text:
            raise CandidateCreationError("Resume text cannot be empty.")

        if not clean_interview_type:
            raise CandidateCreationError("Interview type cannot be recognize.")

        candidate = Candidates(
            name=clean_name,
            email=clean_email,
            resume_filename=clean_resume_filename,
            resume_text=clean_resume_text,
            interview_type=clean_interview_type,
        )

        try:
            db.add(candidate)
            db.commit()
            db.refresh(candidate)

            return candidate

        except SQLAlchemyError as exc:
            db.rollback()

            raise exc

    # -----------------------------------------------------
    # Get Candidate
    # -----------------------------------------------------

    @staticmethod
    def get_candidate(
        db: Session,
        candidate_id: Any,
    ) -> Candidates:

        try:
            candidate = (
                db.query(Candidates).filter(Candidates.id == candidate_id).first()
            )

        except SQLAlchemyError as exc:
            raise CandidateServiceError("Failed to retrieve candidate.") from exc

        if not candidate:
            raise CandidateNotFoundError(
                f"Candidate with id {candidate_id} was not found."
            )

        return candidate

    # -----------------------------------------------------
    # Update Candidate
    # -----------------------------------------------------

    @classmethod
    def update_candidate(
        cls,
        db: Session,
        candidate_id: Any,
        update_data: dict,
    ) -> Candidates:

        candidate = cls.get_candidate(
            db,
            candidate_id,
        )

        # Update name
        if "name" in update_data and update_data["name"] is not None:
            clean_name = update_data["name"].strip()

            if not clean_name:
                raise CandidateUpdateError("Candidate name cannot be empty.")

            candidate.name = clean_name

        # Update email
        if "email" in update_data and update_data["email"] is not None:
            clean_email = update_data["email"].strip().lower()

            if not clean_email:
                raise CandidateUpdateError("Candidate email cannot be empty.")

            candidate.email = clean_email

        try:
            db.commit()
            db.refresh(candidate)

            return candidate

        except SQLAlchemyError as exc:
            db.rollback()

            raise CandidateUpdateError("Failed to update candidate.") from exc
