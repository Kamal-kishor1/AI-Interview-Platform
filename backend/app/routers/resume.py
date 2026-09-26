from fastapi import (
    UploadFile,
    APIRouter,
    File,
    Form,
    Depends,
    status,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.candidate import CandidateResponse

from app.services.candidate_service import (
    CandidateCreationError,
    CandidateNotFoundError,
    CandidateService,
    CandidateServiceError,
)

from app.services.resume_service import (
    CorruptedFileError,
    EmptyDocumentError,
    FileSizeExceededError,
    InvalidFileError,
    ResumeService,
    StorageError,
    UnsupportedFileFormatError,
)

from app.services.interview_type_service import detect_interview_type

router = APIRouter(
    prefix="/api/v1/resumes",
    tags=["resumes"],
)


@router.post(
    "/upload",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and process candidate resume",
)
async def upload_resume(
    name: str = Form(..., description="Candidate's full name"),
    email: str = Form(..., description="Candidate's email address"),
    file: UploadFile = File(..., description="Resume file (.pdf or .docx)"),
    db: Session = Depends(get_db),
) -> CandidateResponse:

    # 1. Process resume
    try:
        resume_data = await ResumeService.process_resume(file)

    except (
        InvalidFileError,
        UnsupportedFileFormatError,
        CorruptedFileError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except FileSizeExceededError as exc:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(exc),
        )

    except EmptyDocumentError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )

    except StorageError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )

    # 2. Detect interview type
    interview_type_data = detect_interview_type(resume_data["extracted_text"])

    interview_type = interview_type_data["interview_type"]

    # 3. Create candidate
    try:
        candidate = CandidateService.create_candidate(
            db=db,
            name=name,
            email=email,
            resume_filename=resume_data["original_filename"],
            resume_text=resume_data["extracted_text"],
            interview_type=interview_type,
        )

        return candidate

    except CandidateCreationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except CandidateNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except CandidateServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
