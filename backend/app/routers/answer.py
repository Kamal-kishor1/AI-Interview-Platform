from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.answer import AnswerCreate, AnswerSubmitResponse

from app.services.answer_service import (
    AnswerCreationError,
    AnswerService,
    DuplicateAnswerError,
    InterviewNotActiveError,
    InterviewNotFoundError,
    InvalidQuestionError,
    QuestionNotFoundError,
)

router = APIRouter(prefix="/api/v1/interviews", tags=["answers"])


@router.post(
    "/{interview_id}/answers",
    response_model=AnswerSubmitResponse,
    status_code=status.HTTP_201_CREATED,
    summary=" Submit an interview answer",
)
def submit_answer(
    interview_id: int, answer_data: AnswerCreate, db: Session = Depends(get_db)
) -> AnswerSubmitResponse:

    try:
        result = AnswerService.submit_answer(
            db=db,
            interview_id=interview_id,
            question_id=answer_data.question_id,
            answer_text=answer_data.answer_text,
        )

        return result

    except InterviewNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except QuestionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except InterviewNotActiveError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    except DuplicateAnswerError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    except InvalidQuestionError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except AnswerCreationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
