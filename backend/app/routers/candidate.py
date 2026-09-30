from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.candidate import CandidateResponse
from app.schemas.candidate_context import CandidateContext

from app.services.candidate_context_service import CandidateContextService
from app.services.candidate_service import CandidateService, CandidateNotFoundError

router = APIRouter(
    prefix="/api/v1/candidates",
    tags=["candidate"],
)


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the candidates.",
)
def get_candidate(
    candidate_id: int, db: Session = Depends(get_db)
) -> CandidateResponse:

    try:
        return CandidateService.get_candidate(db=db, candidate_id=candidate_id)

    except CandidateNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get(
    "/{candidate_id}/context",
    response_model=CandidateContext,
    status_code=status.HTTP_200_OK,
    summary="Get candidate context",
)
async def get_candidate_context(
    candidate_id: int, db: Session = Depends(get_db)
) -> CandidateContext:

    try:
        return await CandidateContextService.build_context(
            db=db, candidate_id=candidate_id
        )

    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
