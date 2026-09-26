from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.candidate import Candidates
from app.models.interview import Interview
from app.models.question import Question


class InterviewServiceError(Exception):
    """Base exception for interview service errors."""


class CandidateNotFoundError(InterviewServiceError):
    """Raised when the candidate does not exist."""


class NoQuestionsAvailableError(InterviewServiceError):
    """Raised when no questions are available for the interview type."""


class InterviewCreationError(InterviewServiceError):
    """Raised when an interview cannot be created."""


class InterviewService:

    @staticmethod
    def start_interview(db: Session, candidate_id: int) -> dict:

        # 1. find candidate

        candidate = db.query(Candidates).filter(Candidates.id == candidate_id).first()

        if not candidate:
            raise CandidateNotFoundError(
                f"Candidate with id {candidate_id} was not found."
            )

        # 2. get interview_type

        interview_type = candidate.interview_type

        if not interview_type:
            raise InterviewCreationError("Candidate does not have an interview type.")

        # 3. get questions

        questions = (
            db.query(Question)
            .filter(Question.interview_type == interview_type)
            .order_by(Question.question_order.asc())
            .all()
        )

        if not questions:
            raise NoQuestionsAvailableError(
                f"No questions available for interview type " f" {interview_type} ."
            )

        # 4. create interview
        interview = Interview(
            candidate_id=candidate.id,
            interview_type=interview_type,
            status="IN_PROGRESS",
            started_at=datetime.now(timezone.utc),
        )

        try:
            db.add(interview)
            db.commit()
            db.refresh(interview)

        except SQLAlchemyError as exc:
            db.rollback()

            raise InterviewCreationError("Failed to create interview.") from exc

        # 5. return first question
        first_question = questions[0]

        return {
            "interview_id": interview.id,
            "interview_type": interview.interview_type,
            "question_id": first_question.id,
            "question_number": 1,
            "total_questions": len(questions),
            "question_text": first_question.question_text,
        }
