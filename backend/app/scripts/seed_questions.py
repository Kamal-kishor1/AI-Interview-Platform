from app.core.database import SessionLocal
from app.services.question_seed_service import (
    QuestionSeedService,
    QuestionSeedServiceError,
)


def main():
    db = SessionLocal()

    try:
        inserted_count = QuestionSeedService.seed_questions(db)

        if inserted_count == 0:
            print("Question bank already contains data. Nothing inserted.")
        else:
            print(f"Successfully seeded {inserted_count} questions.")

    except QuestionSeedServiceError as exc:
        print(f"Question seeding failed: {exc}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
