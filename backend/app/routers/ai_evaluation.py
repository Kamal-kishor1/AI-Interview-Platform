from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.evaluation import EvaluationResponse

from app.services.ai_evaluation_service import (
    AIEvaluationService,
    AIEvaluationDatabaseError,
    AnswerNotFoundError,
    QuestionNotFoundError,
)

from app.services.evaluation_service import (
    EvaluationAlreadyExistsError,
    EvaluationDatabaseError,
    InvalidScoreError,
)

router = APIRouter(
    prefix="/api/v1/evaluations/answer",
    tags=["evaluation"],
)


@router.post(
    "/{answer_id}/ai",
    response_model=EvaluationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an AI evaluation for an answer.",
)
def create_ai_evaluation(
    answer_id: int,
    db: Session = Depends(get_db),
) -> EvaluationResponse:

    try:
        return AIEvaluationService.evaluate_answer(
            answer_id=answer_id,
            db=db,
        )

    except AnswerNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except QuestionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except EvaluationAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except InvalidScoreError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except EvaluationDatabaseError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    except AIEvaluationDatabaseError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


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
        return AIEvaluationService.get_ai_evaluation_by_answer_id(
            db=db, answer_id=answer_id
        )

    except AnswerNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except AIEvaluationDatabaseError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
