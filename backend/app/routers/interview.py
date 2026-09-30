from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.interview import (
    InterviewCreate,
    InterviewQuestionResponse,
)
from app.services.interview_service import (
    CandidateNotFoundError,
    InterviewCreationError,
    InterviewService,
    NoQuestionsAvailableError,
    InterviewNotFoundError,
)

router = APIRouter(
    prefix="/api/v1/interviews",
    tags=["interviews"],
)


@router.post(
    "/start",
    response_model=InterviewQuestionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start an interview",
)
def start_interview(
    interview_data: InterviewCreate, db: Session = Depends(get_db)
) -> InterviewQuestionResponse:

    try:
        result = InterviewService.start_interview(db=db, interview_data=interview_data)

        return result

    except CandidateNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except NoQuestionsAvailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except InterviewCreationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/{interview_id}/current-question",
    response_model=InterviewQuestionResponse,
    summary="Get current interview question",
)
def get_current_question(
    interview_id: int, db: Session = Depends(get_db)
) -> InterviewQuestionResponse:

    try:
        result = InterviewService.get_current_question(db=db, interview_id=interview_id)

        return result

    except InterviewNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    except NoQuestionsAvailableError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
