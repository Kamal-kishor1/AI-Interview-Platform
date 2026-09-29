from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.models.interview import Interview
from app.models.question import Question
from app.models.candidate import Candidates

from app.services.answer_service import InterviewNotFoundError

from app.services.ai_evaluation_service import (
    AIEvaluationService,
    EvaluationNotFoundError,
)


class CompletionNotFound:
    """Your interview is not completed yet."""


class InterviewResultService:

    @staticmethod
    def result(db: Session, interview_id: int) -> dict:

        # 1. Retrieve the interview

        interview = db.query(Interview).filter(Interview.id == interview_id).first()

        if not interview:
            raise InterviewNotFoundError(
                f"Interview with id {interview_id} was not found."
            )

        # 2. Retrieve candidate belonging to this interview
        candidate = (
            db.query(Candidates).filter(Candidates.id == interview.candidate_id).first()
        )

        # 3. Retrieve all questions belonging to this interview type

        questions = (
            db.query(Question)
            .filter(Question.interview_type == interview.interview_type)
            .order_by(Question.question_order.asc())
            .all()
        )

        # 4. Retrieve all answers submitted for this interview

        answers = db.query(Answer).filter(Answer.interview_id == interview.id).all()

        answered_questions = len(answers)
        total_questions = len(questions)

        # 5. Calculate interview completion percentage

        if total_questions == 0:
            completion_percentage = 0.0
        else:
            completion_percentage = round(
                (answered_questions / total_questions) * 100,
                2,
            )

        # 6. Calculate interview duration

        duration_seconds = None

        if interview.started_at:
            end_time = interview.completed_at

            if end_time is None:
                end_time = datetime.now(timezone.utc)

            duration = end_time - interview.started_at
            duration_seconds = int(duration.total_seconds())

        # 7. Build evaluation data for every answer
        evaluations = []

        for answer in answers:
            try:
                evaluation = AIEvaluationService.get_ai_evaluation_by_answer_id(
                    db=db, answer_id=answer.id
                )

            except EvaluationNotFoundError:

                # The MVP normally evaluates every answer.
                # If an evaluation is missing, keep the answer
                # in the result instead of failing the whole result.
                evaluation = None

            # Find the question belonging to this answer.
            question = (
                db.query(Question).filter(Question.id == answer.question_id).first()
            )

            evaluations.append(
                {
                    "answer_id": answer.id,
                    "question_id": answer.question_id,
                    "question_text": (question.question_text if question else None),
                    "answer_text": answer.answer_text,
                    "evaluation": evaluation,
                }
            )

        # 8. Calculate overall interview score.
        evaluated_scores = [
            item["evaluation"].overall_score
            for item in evaluations
            if item["evaluation"] is not None
        ]

        if evaluated_scores:
            overall_score = round(
                sum(evaluated_scores) / len(evaluated_scores),
                2,
            )
        else:
            overall_score = None

        # 9. Return complete interview result.

        return {
            "interview_id": interview.id,
            "candidate_id": interview.candidate_id,
            "candidate_name": (candidate.name if candidate else None),
            "interview_type": interview.interview_type,
            "status": interview.status,
            "total_questions": total_questions,
            "answered_questions": answered_questions,
            "completion_percentage": completion_percentage,
            "overall_score": overall_score,
            "evaluations": evaluations,
            "started_at": interview.started_at,
            "completed_at": interview.completed_at,
            "duration_seconds": duration_seconds,
        }
