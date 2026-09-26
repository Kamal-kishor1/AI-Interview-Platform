from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.interview import (
    InterviewCreate,
    InterviewStartResponse,
)
from app.services.interview_service import (
    CandidateNotFoundError,
    InterviewCreationError,
    InterviewService,
    NoQuestionsAvailableError,
)

router = APIRouter(
    prefix="/api/v1/interviews",
    tags=["interviews"],
)


@router.post(
    "/start",
    response_model=InterviewStartResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start an interview",
)
def start_interview(
    interview_data: InterviewCreate, db: Session = Depends(get_db)
) -> InterviewStartResponse:

    try:
        result = InterviewService.start_interview(
            db=db, candidate_id=interview_data.candidate_id
        )

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
