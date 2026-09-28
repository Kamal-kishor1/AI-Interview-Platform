from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.evaluation import EvaluationCreate, EvaluationResponse

from app.services.evaluation_service import (
    EvaluationService,
    AnswerNotFoundError,
    EvaluationAlreadyExistsError,
    InvalidScoreError,
    EvaluationDatabaseError,
)

router = APIRouter(prefix="/api/v1/evaluations", tags=["evaluations"])


@router.post(
    "",
    response_model=EvaluationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an evaluation for an answer",
)
def create_evaluation(
    evalutaion_in: EvaluationCreate, db: Session = Depends(get_db)
) -> EvaluationResponse:

    try:
        return EvaluationService.create_evaluation(db=db, evaluation_in=evalutaion_in)

    except AnswerNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except EvaluationAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
    except InvalidScoreError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except EvaluationDatabaseError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.get(
    "/answer/{answer_id}",
    response_model=EvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get evaluation by answer ID",
)
def get_evaluation_by_answer(
    answer_id: int,
    db: Session = Depends(get_db),
) -> EvaluationResponse:

    try:
        return EvaluationService.get_evaluation_by_answer_id(db=db, answer_id=answer_id)

    except AnswerNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except EvaluationDatabaseError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
