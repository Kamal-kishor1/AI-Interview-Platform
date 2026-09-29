from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.models.interview import Interview
from app.models.question import Question

from app.services.ai_evaluation_service import (
    AIEvaluationService,
    AIEvaluationDatabaseError,
    AnswerNotFoundError as AIEvaluationAnswerNotFoundError,
    QuestionNotFoundError as AIEvaluationQuestionNotFoundError,
)

"""
One limitation of the current MVP

The service determines the question sequence from:

Question.interview_type == interview.interview_type

So every AI/ML interview currently uses the same 15-question sequence.

That is intentional for the MVP.

Later, we can introduce an interview_questions table so each interview gets its own fixed question set.
That will become important when we add randomized or AI-generated questions.

"""


class AnswerServiceError(Exception):
    """Base exception for answer service errors."""


class InterviewNotFoundError(AnswerServiceError):
    """Raised when the interview does not exist."""


class InterviewNotActiveError(AnswerServiceError):
    """Raised when the interview is not in progress."""


class QuestionNotFoundError(AnswerServiceError):
    """Raised when the question does not exist."""


class InvalidQuestionError(AnswerServiceError):
    """Raised when the question does not belong to the interview."""


class DuplicateAnswerError(AnswerServiceError):
    """Raised when a question has already been answered."""


class AnswerCreationError(AnswerServiceError):
    """Raised when an answer cannot be saved."""


class AIProviderError(AnswerServiceError):
    """Raised  when AI Provider fails."""


class AnswerService:

    @staticmethod
    def submit_answer(
        db: Session, interview_id: int, question_id: int, answer_text: str
    ) -> dict:

        # 1. validate answer text
        clean_answer = answer_text.strip()

        if not clean_answer:
            raise AnswerCreationError("Answer cannot be empty.")

        # 2. find interview

        interview = db.query(Interview).filter(Interview.id == interview_id).first()

        if not interview:
            raise InterviewNotFoundError(
                f"Interview with id {interview_id} was not found."
            )

        # 3. Interview must be active

        if interview.status != "IN_PROGRESS":
            raise InterviewNotActiveError(
                f"Interview is not active. Current Status: {interview.status}"
            )

        # 4. find question

        question = db.query(Question).filter(Question.id == question_id).first()

        if not question:
            raise QuestionNotFoundError(
                f" Question with id {question_id} was not found."
            )

        # 5. verify question belongs to interview type

        if question.interview_type != interview.interview_type:
            raise InvalidQuestionError("Question does not belong to this interview.")

        # 6. Prevent duplicate answers

        existing_answer = (
            db.query(Answer)
            .filter(
                Answer.interview_id == interview_id,
                Answer.question_id == question_id,
            )
            .first()
        )

        if existing_answer:
            raise DuplicateAnswerError("This question has already been answered.")

        # 7. create answer
        answer = Answer(
            interview_id=interview_id, question_id=question_id, answer_text=clean_answer
        )

        try:
            # Add answer to the SQLALchemy session

            db.add(answer)

            # Flush so Postgressql generates answer.id
            # without committing the transaction yet.

            db.flush()

            """ New step to integrate the ai-evaluation """

            # i) Evaluate the saved answer using AI

            try:

                evaluation = AIEvaluationService.evaluate_answer(
                    answer_id=answer.id, db=db
                )

            except (
                AIEvaluationAnswerNotFoundError,
                AIEvaluationQuestionNotFoundError,
                AIEvaluationDatabaseError,
                RuntimeError,
            ) as exc:
                raise AIProviderError(
                    "AI evaluation failed for the submitted answer."
                ) from exc

            # 8. find all question for this interview

            questions = (
                db.query(Question)
                .filter(Question.interview_type == interview.interview_type)
                .order_by(Question.question_order.asc())
                .all()
            )

            # 9. Find current question position

            current_index = next(
                (
                    index
                    for index, item in enumerate(questions)
                    if item.id == question_id
                ),
                None,
            )

            if current_index is None:
                raise InvalidQuestionError(
                    "Question is not part of the interview question set."
                )

            question_number = current_index + 1
            total_questions = len(questions)

            # 10. check whether this is the final question
            if current_index == total_questions - 1:

                interview.status = "COMPLETED"
                interview.completed_at = datetime.now(timezone.utc)

                db.commit()
                db.refresh(answer)

                return {
                    "answer_id": answer.id,
                    "interview_id": interview_id,
                    "question_id": question_id,
                    "question_number": question_number,
                    "total_questions": total_questions,
                    "answer_saved": True,
                    "interview_completed": True,
                    "evaluation": evaluation,
                    "next_question_id": None,
                    "next_question_number": None,
                    "next_question_text": None,
                }

            # 11. get next question
            next_question = questions[current_index + 1]

            db.commit()
            db.refresh(answer)

            return {
                "answer_id": answer.id,
                "interview_id": interview_id,
                "question_id": question_id,
                "question_number": question_number,
                "total_questions": total_questions,
                "answer_saved": True,
                "interview_completed": False,
                "evaluation": evaluation,
                "next_question_id": next_question.id,
                "next_question_number": question_number + 1,
                "next_question_text": next_question.question_text,
            }

        except AnswerServiceError:
            db.rollback()
            raise

        except SQLAlchemyError as exc:
            db.rollback()

            raise AnswerCreationError("Failed to save answer.") from exc
