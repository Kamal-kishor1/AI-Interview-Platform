from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.models.interview import Interview
from app.models.question import Question
from app.services.answer_service import InterviewNotFoundError
from app.models.candidate import Candidates


class CompletionNotFound:
    """Your interview is not completed yet."""


class InterviewResultService:

    @staticmethod
    def result(db: Session, interview_id: int) -> dict:

        interview = db.query(Interview).filter(Interview.id == interview_id).first()

        if not interview:
            raise InterviewNotFoundError(
                f"Interview with id {interview_id} was not found."
            )

        # Get candidate belonging to this interview
        candidate = (
            db.query(Candidates).filter(Candidates.id == interview.candidate_id).first()
        )

        questions = (
            db.query(Question)
            .filter(Question.interview_type == interview.interview_type)
            .order_by(Question.question_order.asc())
            .all()
        )

        answers = db.query(Answer).filter(Answer.interview_id == interview.id).all()

        answered_questions = len(answers)
        total_questions = len(questions)

        if total_questions == 0:
            completion_percentage = 0.0
        else:
            completion_percentage = round(
                (answered_questions / total_questions) * 100,
                2,
            )

        duration_seconds = None

        if interview.started_at:
            end_time = interview.completed_at

            if end_time is None:
                end_time = datetime.now(timezone.utc)

            duration = end_time - interview.started_at
            duration_seconds = int(duration.total_seconds())

        return {
            "interview_id": interview.id,
            "candidate_id": interview.candidate_id,
            "candidate_name": candidate.name if candidate else None,
            "interview_type": interview.interview_type,
            "status": interview.status,
            "total_questions": total_questions,
            "answered_questions": answered_questions,
            "completion_percentage": completion_percentage,
            "started_at": interview.started_at,
            "completed_at": interview.completed_at,
            "duration_seconds": duration_seconds,
        }
