from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.models.candidate import Candidates
from app.models.interview import Interview
from app.models.question import Question

from app.schemas.interview import InterviewCreate


class InterviewServiceError(Exception):
    """Base exception for interview service errors."""


class InterviewNotFoundError(InterviewServiceError):
    """Raised when an interview does not exist."""


class CandidateNotFoundError(InterviewServiceError):
    """Raised when the candidate does not exist."""


class NoQuestionsAvailableError(InterviewServiceError):
    """Raised when no questions are available for the interview type."""


class InterviewCompletedError(InterviewServiceError):
    """Raised when an interview has no unanswered questions remaining."""


class InterviewCreationError(InterviewServiceError):
    """Raised when an interview cannot be created."""


class InterviewService:

    @staticmethod
    def _get_questions(
        db: Session,
        interview_type: str,
    ) -> list[Question]:

        return (
            db.query(Question)
            .filter(Question.interview_type == interview_type)
            .order_by(Question.question_order.asc())
            .all()
        )

    @staticmethod
    def start_interview(
        db: Session,
        interview_data: InterviewCreate,
    ) -> dict:

        # 1. Find candidate
        candidate = (
            db.query(Candidates)
            .filter(Candidates.id == interview_data.candidate_id)
            .first()
        )

        if not candidate:
            raise CandidateNotFoundError(
                f"Candidate with id {interview_data.candidate_id} was not found."
            )

        # 2. Get interview type
        interview_type = candidate.interview_type

        if not interview_type:
            raise InterviewCreationError("Candidate does not have an interview type.")

        # 3. Get questions
        questions = InterviewService._get_questions(
            db=db,
            interview_type=interview_type,
        )

        if not questions:
            raise NoQuestionsAvailableError(
                f"No questions available for interview type " f"{interview_type}."
            )

        # i) existing active interview
        existing_interview = (
            db.query(Interview)
            .filter(Interview.candidate_id == candidate.id)
            .order_by(Interview.created_at.desc())
            .first()
        )

        # ii) Handle existing interview
        if existing_interview:

            # already started: do not create another interview.

            if existing_interview.status == "IN_PROGRESS":
                interview = existing_interview

            # pending: resuse it, apply latest configuration, and move it to in_progress
            elif existing_interview.status == "PENDING":

                existing_interview.difficulty = interview_data.difficulty
                existing_interview.question_count = interview_data.question_count
                existing_interview.use_skills = interview_data.use_skills
                existing_interview.use_projects = interview_data.use_projects
                existing_interview.use_experience = interview_data.use_experience
                existing_interview.use_resume = interview_data.use_resume

                existing_interview.status = "IN_PROGRESS"
                existing_interview.started_at = datetime.now(timezone.utc)

                interview = existing_interview

            # completed interview: for now allow creation of a new interview
            elif existing_interview.status == "COMPLETED":

                interview = Interview(
                    candidate_id=candidate.id,
                    interview_type=interview_type,
                    status="IN_PROGRESS",
                    difficulty=interview_data.difficulty,
                    question_count=interview_data.question_count,
                    use_skills=interview_data.use_skills,
                    use_projects=interview_data.use_projects,
                    use_experience=interview_data.use_experience,
                    use_resume=interview_data.use_resume,
                    started_at=datetime.now(timezone.utc),
                )

            else:
                raise InterviewCreationError(
                    f"Interview has unsupported status: {existing_interview.status}"
                )

        else:
            interview = Interview(
                candidate_id=candidate.id,
                interview_type=interview_type,
                status="IN_PROGRESS",
                difficulty=interview_data.difficulty,
                question_count=interview_data.question_count,
                use_skills=interview_data.use_skills,
                use_projects=interview_data.use_projects,
                use_experience=interview_data.use_experience,
                use_resume=interview_data.use_resume,
                started_at=datetime.now(timezone.utc),
            )

        # 7. persist changes

        try:
            db.add(interview)
            db.commit()
            db.refresh(interview)

        except SQLAlchemyError as exc:
            db.rollback()
            raise InterviewCreationError("Failed to create interview.") from exc

        # 5. Return first question
        first_question = questions[0]

        return {
            "interview_id": interview.id,
            "interview_type": interview.interview_type,
            "question_id": first_question.id,
            "question_number": 1,
            "total_questions": len(questions),
            "question_text": first_question.question_text,
        }

    @staticmethod
    def get_current_question(
        db: Session,
        interview_id: int,
    ) -> dict:

        # 1. Find interview
        interview = db.query(Interview).filter(Interview.id == interview_id).first()

        if not interview:
            raise InterviewNotFoundError(
                f"Interview with id {interview_id} was not found."
            )

        # 2. Get questions
        questions = InterviewService._get_questions(
            db=db,
            interview_type=interview.interview_type,
        )

        if not questions:
            raise NoQuestionsAvailableError(
                f"No questions available for interview type "
                f"{interview.interview_type}."
            )

        # 3. Get answered question IDs
        answers = db.query(Answer).filter(Answer.interview_id == interview.id).all()

        answered_question_ids = {answer.question_id for answer in answers}

        # 4. Find first unanswered question
        current_question = next(
            (
                question
                for question in questions
                if question.id not in answered_question_ids
            ),
            None,
        )

        if current_question is None:
            raise InterviewCompletedError("This interview has already been completed.")

        # 5. Determine question number
        question_number = next(
            index
            for index, question in enumerate(questions, start=1)
            if question.id == current_question.id
        )

        return {
            "interview_id": interview.id,
            "interview_type": interview.interview_type,
            "question_id": current_question.id,
            "question_number": question_number,
            "total_questions": len(questions),
            "question_text": current_question.question_text,
        }
