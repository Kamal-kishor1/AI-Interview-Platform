from abc import ABC, abstractmethod

from app.schemas.ai_evaluation import AIEvaluationResponse
from app.schemas.candidate_context import CandidateContextExtraction


class AIProvider(ABC):
    """Base interface for AI providers."""

    @abstractmethod
    def evaluate_answer(
        self,
        question_text: str,
        answer_text: str,
    ) -> AIEvaluationResponse:
        """
        Evaluate a candidate's answer against a question.

        Args:
            question_text: The interview question.
            answer_text: The candidate's submitted answer.

        Returns:
            A structured AI evaluation.
        """
        raise NotImplementedError

    @abstractmethod
    async def extract_candidate_context(
        self, resume_text: str
    ) -> CandidateContextExtraction:
        """Extract structured candidate context from resume text."""
        raise NotImplementedError
