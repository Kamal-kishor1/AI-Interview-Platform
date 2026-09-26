from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.result import InterviewResultResponse
from app.services.interview_result_service import InterviewResultService

from app.services.answer_service import InterviewNotFoundError

router = APIRouter(prefix="/api/v1/interviews", tags=["interview-results"])


@router.get(
    "/{interview_id}/result",
    response_model=InterviewResultResponse,
    status_code=status.HTTP_200_OK,
    summary="Get interview result ",
)
def get_interview_result(
    interview_id: int, db: Session = Depends(get_db)
) -> InterviewResultResponse:

    try:

        result = InterviewResultService.result(db=db, interview_id=interview_id)

        return result

    except InterviewNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
