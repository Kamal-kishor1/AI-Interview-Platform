from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationCreate


class EvaluationServiceError(Exception):
    """Base exception for evaluation service errors."""


class InvalidScoreError(EvaluationServiceError):
    """Raised when a score falls outside the 0.0 - 10.0 range."""


class AnswerNotFoundError(EvaluationServiceError):
    """Raised when the target answer does not exist."""


class EvaluationNotFoundError(EvaluationServiceError):
    """Raised when an evaluation does not exist."""


class EvaluationAlreadyExistsError(EvaluationServiceError):
    """Raised when the answer has already been evaluated."""


class EvaluationDatabaseError(EvaluationServiceError):
    """Raised when database commit or session operations fail."""


class EvaluationService:

    @staticmethod
    def _validate_score(score: float, field_name: str) -> None:
        # Validates that a score falls within the allowed 0-10 bounds.
        if score is None or not (0.0 <= score <= 10.0):
            raise InvalidScoreError(
                f"Invalid score for '{field_name}' : {score}. Must be between 0 - 10. "
            )

    @classmethod
    def calculate_overall_score(
        cls, correctness: float, relevance: float, completeness: float, clarity: float
    ) -> float:

        # Calculate deterministic average rounded to 2 decimal places
        cls._validate_score(correctness, "correctness_score")
        cls._validate_score(relevance, "relevance_score")
        cls._validate_score(completeness, "completeness_score")
        cls._validate_score(clarity, "clarity_score")

        overall_score = (correctness + relevance + completeness + clarity) / 4.0

        return round(overall_score, 2)

    @classmethod
    def create_evaluation(
        cls, db: Session, evaluation_in: EvaluationCreate
    ) -> Evaluation:

        # Validates scores, checks answer existence, prevents duplicates,
        # computes overall score and persists the evaluation.

        # 1. verify that the answer exists
        answer = db.query(Answer).filter(Answer.id == evaluation_in.answer_id).first()

        if not answer:
            raise AnswerNotFoundError(
                f"Answer with id {evaluation_in.answer_id} does not exist."
            )

        # 2. check if this sanswer was already evaluated
        existing_answer = (
            db.query(Evaluation)
            .filter(Evaluation.answer_id == evaluation_in.answer_id)
            .first()
        )

        if existing_answer:
            raise EvaluationAlreadyExistsError(
                f"Answer {evaluation_in.answer_id} has already been evaluated."
            )

        # 3. Calculate overall score (enforeces 0-10 validation)
        overall = cls.calculate_overall_score(
            correctness=evaluation_in.correctness_score,
            relevance=evaluation_in.relevance_score,
            completeness=evaluation_in.completeness_score,
            clarity=evaluation_in.clarity_score,
        )

        # 4. Construct model
        evaluation = Evaluation(
            answer_id=evaluation_in.answer_id,
            correctness_score=evaluation_in.correctness_score,
            relevance_score=evaluation_in.relevance_score,
            completeness_score=evaluation_in.completeness_score,
            clarity_score=evaluation_in.clarity_score,
            overall_score=overall,
            strengths=evaluation_in.strengths.strip(),
            weaknesses=evaluation_in.weaknesses.strip(),
            improvement_feedback=evaluation_in.improvement_feedback.strip(),
        )

        try:
            db.add(evaluation)
            db.commit()
            db.refresh(evaluation)
            return evaluation

        except IntegrityError as exc:
            db.rollback()
            raise EvaluationAlreadyExistsError(
                f"Unique constraint violation: Answer {evaluation_in.answer_id} already evaluated."
            ) from exc

        except SQLAlchemyError as exc:
            db.rollback()
            raise EvaluationDatabaseError(
                f"Database error while saving evaluation: {exc}"
            ) from exc

    @classmethod
    def get_evaluation_by_answer_id(cls, db: Session, answer_id: int) -> Evaluation:
        """Retrieves evaluation for a given answer ID."""

        try:
            evaluation = (
                db.query(Evaluation).filter(Evaluation.answer_id == answer_id).first()
            )
        except SQLAlchemyError as exc:
            raise EvaluationDatabaseError(
                f"Database error retrieving evaluation: {exc}"
            ) from exc

        if not evaluation:
            raise EvaluationNotFoundError(
                f"Evaluation for answer id {answer_id} not found."
            )

        return evaluation
