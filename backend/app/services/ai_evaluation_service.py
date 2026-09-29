from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.answer import Answer
from app.models.question import Question
from app.models.evaluation import Evaluation
from app.providers.ai.groq import GroqProvider

from app.schemas.evaluation import EvaluationCreate
from app.schemas.ai_evaluation import AIEvaluationResponse
from app.services.evaluation_service import EvaluationService


class AIEvaluationServiceError(Exception):
    """Base exception for AI evaluation service errors."""


class AnswerNotFoundError(AIEvaluationServiceError):
    """Raised when the target answer does not exist."""


class QuestionNotFoundError(AIEvaluationServiceError):
    """Raised when the question associated with the answer does not exist."""


class AIEvaluationDatabaseError(AIEvaluationServiceError):
    """Raised when a database operation fails during AI evaluation."""


class EvaluationNotFoundError(AIEvaluationServiceError):
    """Raised when an evaluation does not exist."""


class AIEvaluationService:

    @staticmethod
    def _get_answer_and_question(
        answer_id: int,
        db: Session,
    ) -> tuple[Answer, Question]:

        # Retrieve the answer and its associated question.

        try:
            # 1. Retrieve answer from database
            answer = db.query(Answer).filter(Answer.id == answer_id).first()

            if not answer:
                raise AnswerNotFoundError(f"Answer with id {answer_id} not found.")

            # 2. Retrieve question from database
            question = (
                db.query(Question).filter(Question.id == answer.question_id).first()
            )

            if not question:
                raise QuestionNotFoundError(
                    f"Question with id {answer.question_id} not found."
                )

            return answer, question

        except SQLAlchemyError as exc:
            raise AIEvaluationDatabaseError(
                "Database error while retrieving answer and question."
            ) from exc

    @classmethod
    def evaluate_answer(
        cls,
        answer_id: int,
        db: Session,
    ) -> Evaluation:

        # 1. Retrieve answer and question
        answer, question = cls._get_answer_and_question(
            answer_id=answer_id,
            db=db,
        )

        # 2. Evaluate answer using Groq
        provider = GroqProvider()

        ai_result: AIEvaluationResponse = provider.evaluate_answer(
            question_text=question.question_text,
            answer_text=answer.answer_text,
        )

        # 3. Convert AI response into database evaluation data
        evaluation_data = EvaluationCreate(
            answer_id=answer.id,
            correctness_score=ai_result.correctness_score,
            relevance_score=ai_result.relevance_score,
            completeness_score=ai_result.completeness_score,
            clarity_score=ai_result.clarity_score,
            strengths=ai_result.strengths.strip(),
            weaknesses=ai_result.weaknesses.strip(),
            improvement_feedback=ai_result.improvement_feedback.strip(),
        )

        # 4. Save evaluation.
        # EvaluationService calculates overall_score and persists the record.
        evaluation = EvaluationService.create_evaluation(
            db=db,
            evaluation_in=evaluation_data,
        )

        # 5. Return the saved database evaluation
        return evaluation

    @classmethod
    def get_ai_evaluation_by_answer_id(cls, db: Session, answer_id: int) -> Evaluation:
        """Retrieves ai evaluation for a given answer ID."""

        try:
            evaluation = (
                db.query(Evaluation).filter(Evaluation.answer_id == answer_id).first()
            )

        except SQLAlchemyError as exc:
            raise AIEvaluationDatabaseError(
                f"Database error retrieving evaluation: {exc}"
            ) from exc

        if not evaluation:
            raise EvaluationNotFoundError(
                f"Evaluation for answer id {answer_id} not found."
            )

        return evaluation
