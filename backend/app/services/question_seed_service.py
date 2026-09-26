from unicodedata import category

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.data.question_bank import QUESTION_BANKS
from app.models.question import Question


class QuestionSeedServiceError(Exception):
    """Base exception for question seeding errors."""


class QuestionSeedService:

    @staticmethod
    def seed_questions(db: Session) -> int:
        """
        Seed all question from the hardcoded question bank.
        Returns:
            Number of question inserted.

        """

        try:
            # prevent duplicate seeding.
            existing_count = db.query(Question).count()

            if existing_count > 0:
                return 0

            questions_to_insert = []

            for interview_type, question_bank in QUESTION_BANKS.items():

                for question_order, question_data in enumerate(question_bank, start=1):
                    question = Question(
                        interview_type=interview_type,
                        category=question_data["category"],
                        question_text=question_data["question_text"],
                        difficulty=question_data["difficulty"],
                        question_order=question_order,
                    )

                    questions_to_insert.append(question)

            db.add_all(questions_to_insert)
            db.commit()

            return len(questions_to_insert)

        except SQLAlchemyError as exc:
            db.rollback()

            raise QuestionSeedServiceError("Failed to seed question bank.") from exc
