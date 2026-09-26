from pathlib import Path
import re
from uuid import uuid4

from docx import Document
from fastapi import UploadFile
from pypdf import PdfReader

from app.core.config import settings

# ---------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------


class ResumeServiceError(Exception):
    """Base exception for ResumeService errors."""


class InvalidFileError(ResumeServiceError):
    """Raised when the uploaded file is missing or invalid."""


class UnsupportedFileFormatError(ResumeServiceError):
    """Raised when the uploaded file format is not supported."""


class FileSizeExceededError(ResumeServiceError):
    """Raised when the uploaded file exceeds the maximum size."""


class EmptyDocumentError(ResumeServiceError):
    """Raised when no readable text can be extracted."""


class CorruptedFileError(ResumeServiceError):
    """Raised when the uploaded document cannot be parsed."""


class StorageError(ResumeServiceError):
    """Raised when file storage operations fail."""


# ---------------------------------------------------------
# Resume Service
# ---------------------------------------------------------


class ResumeService:

    SUPPORTED_EXTENSIONS = {".pdf", ".docx"}

    MAX_FILE_SIZE = getattr(
        settings,
        "MAX_UPLOAD_SIZE_BYTES",
        5 * 1024 * 1024,
    )

    UPLOAD_DIR = Path(
        getattr(
            settings,
            "UPLOAD_DIR",
            "uploads/resumes",
        )
    )

    # -----------------------------------------------------
    # Directory
    # -----------------------------------------------------

    @classmethod
    def _ensure_upload_directory(cls) -> Path:
        """Create the upload directory if it does not exist."""

        try:
            cls.UPLOAD_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )
            return cls.UPLOAD_DIR

        except OSError as exc:
            raise StorageError(f"Unable to initialize upload directory: {exc}") from exc

    # -----------------------------------------------------
    # File Validation
    # -----------------------------------------------------

    @classmethod
    async def validate_file(cls, file: UploadFile) -> str:
        """
        Validate uploaded resume.

        Returns:
            Normalized file extension.
        """

        if file is None or not file.filename:
            raise InvalidFileError("Resume file was not provided.")

        extension = Path(file.filename).suffix.lower()

        if extension not in cls.SUPPORTED_EXTENSIONS:
            allowed = ", ".join(sorted(cls.SUPPORTED_EXTENSIONS))

            raise UnsupportedFileFormatError(
                f"Unsupported file format '{extension}'. " f"Allowed formats: {allowed}"
            )

        # Check file size
        contents = await file.read()

        if len(contents) > cls.MAX_FILE_SIZE:
            max_mb = cls.MAX_FILE_SIZE / (1024 * 1024)

            raise FileSizeExceededError(
                f"File exceeds the maximum allowed size " f"of {max_mb:.1f} MB."
            )

        # Reset pointer so the file can be read again.
        await file.seek(0)

        return extension

    # -----------------------------------------------------
    # Filename
    # -----------------------------------------------------

    @staticmethod
    def generate_filename(extension: str) -> str:
        """Generate a unique filename."""

        return f"{uuid4().hex}{extension}"

    # -----------------------------------------------------
    # Save File
    # -----------------------------------------------------

    @classmethod
    async def save_file(
        cls,
        file: UploadFile,
        destination: Path,
    ) -> Path:
        """Save uploaded file to disk."""

        try:
            contents = await file.read()

            destination.write_bytes(contents)

            return destination

        except OSError as exc:
            raise StorageError(f"Unable to save resume: {exc}") from exc

        finally:
            await file.seek(0)

    # -----------------------------------------------------
    # PDF Extraction
    # -----------------------------------------------------

    @staticmethod
    def _extract_pdf_text(file_path: Path) -> str:
        """Extract readable text from a PDF."""

        try:
            reader = PdfReader(str(file_path))

            pages_text = []

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    pages_text.append(text)

            combined_text = "\n".join(pages_text).strip()

            if not combined_text:
                raise EmptyDocumentError(
                    "Could not extract text from the PDF. "
                    "The resume may be scanned or image-only."
                )

            return combined_text

        except EmptyDocumentError:
            raise

        except Exception as exc:
            raise CorruptedFileError(f"Failed to parse PDF document: {exc}") from exc

    # -----------------------------------------------------
    # DOCX Extraction
    # -----------------------------------------------------

    @staticmethod
    def _extract_docx_text(file_path: Path) -> str:
        """Extract readable text from a DOCX document."""

        try:
            document = Document(str(file_path))

            paragraphs = []

            for paragraph in document.paragraphs:

                text = paragraph.text.strip()

                if text:
                    paragraphs.append(text)

            combined_text = "\n".join(paragraphs).strip()

            if not combined_text:
                raise EmptyDocumentError(
                    "Could not extract text from the DOCX document."
                )

            return combined_text

        except EmptyDocumentError:
            raise

        except Exception as exc:
            raise CorruptedFileError(f"Failed to parse DOCX document: {exc}") from exc

    # -----------------------------------------------------
    # Text Cleaning
    # -----------------------------------------------------

    @staticmethod
    def _clean_text(text: str) -> str:
        """Normalize extracted resume text."""

        # Normalize spaces and tabs.
        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        # Normalize excessive blank lines.
        text = re.sub(
            r"\n\s*\n\s*\n+",
            "\n\n",
            text,
        )

        return text.strip()

    # -----------------------------------------------------
    # Main Processing Pipeline
    # -----------------------------------------------------

    @classmethod
    async def process_resume(
        cls,
        file: UploadFile,
    ) -> dict:
        """
        Validate, store, extract, and clean a resume.

        Returns:
            Resume processing metadata and extracted text.
        """

        # 1. Validate
        extension = await cls.validate_file(file)

        # 2. Prepare storage
        upload_dir = cls._ensure_upload_directory()

        stored_filename = cls.generate_filename(extension)

        target_path = upload_dir / stored_filename

        # 3. Save file
        await cls.save_file(
            file,
            target_path,
        )

        try:

            # 4. Extract text
            if extension == ".pdf":

                raw_text = cls._extract_pdf_text(target_path)

            elif extension == ".docx":

                raw_text = cls._extract_docx_text(target_path)

            else:

                raise UnsupportedFileFormatError(f"Unsupported extension: {extension}")

            # 5. Clean extracted text
            extracted_text = cls._clean_text(raw_text)

            # 6. Final empty-text check
            if not extracted_text:

                raise EmptyDocumentError("Resume contains no readable text.")

            # 7. Return result
            return {
                "original_filename": file.filename,
                "stored_filename": stored_filename,
                "file_path": str(target_path),
                "extracted_text": extracted_text,
            }

        except ResumeServiceError:

            # Delete the stored file if processing failed.
            try:
                target_path.unlink(missing_ok=True)
            except OSError:
                pass

            raise
