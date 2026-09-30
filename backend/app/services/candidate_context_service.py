from sqlalchemy.orm import Session

from app.models.candidate import Candidates

from app.schemas.candidate_context import (
    CandidateContextExtraction,
    CandidateContext,
)

from app.providers.ai.groq import GroqProvider


class CandidateContextService:

    @staticmethod
    async def build_context(db: Session, candidate_id: int) -> CandidateContext:

        # 1. Find candidate

        candidate = db.query(Candidates).filter(Candidates.id == candidate_id).first()

        if not candidate:
            raise ValueError(f"Candidate with id {candidate_id} was not found.")

        # 2. get already-extracted resume text

        resume_text = candidate.resume_text

        if not resume_text:
            raise ValueError(f"Candidate does not have resume text.")

        # 3. Extract structured information

        candidate_context = await CandidateContextService._extract_context(resume_text)

        return CandidateContext(
            skills=candidate_context.skills,
            projects=candidate_context.projects,
            experience=candidate_context.experience,
            resume_text=resume_text,
        )

    @staticmethod
    async def _extract_context(resume_text: str) -> CandidateContextExtraction:

        provider = GroqProvider()

        candidate_context = await provider.extract_candidate_context(
            resume_text=resume_text
        )

        return candidate_context
