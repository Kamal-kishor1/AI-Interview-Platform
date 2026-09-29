from google import genai
from google.genai import types

from app.providers.ai.base import AIProvider
from app.core.config import settings
from app.schemas.ai_evaluation import AIEvaluationResponse


class GeminiProvider(AIProvider):
    """Gemini implementation of the AI evaluation provider."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ):

        self.api_key = api_key or settings.GEMINI_API_KEY

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not configured.")

        self.model = model or settings.GEMINI_MODEL

        if not self.model:
            raise ValueError("GEMINI_MODEL environment variable is not configured.")

        self.client = genai.Client(
            api_key=self.api_key,
        )

    def evaluate_answer(
        self,
        question_text: str,
        answer_text: str,
    ) -> AIEvaluationResponse:

        prompt = self._build_evaluation_prompt(
            question_text=question_text,
            answer_text=answer_text,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AIEvaluationResponse,
            ),
        )

        if not response.parsed:
            raise ValueError("Gemini returned an empty or invalid evaluation response.")

        return response.parsed

    @staticmethod
    def _build_evaluation_prompt(
        question_text: str,
        answer_text: str,
    ) -> str:

        return f"""
You are an expert technical interviewer evaluating a candidate's answer.

Evaluate the candidate's answer against the interview question.

Evaluation criteria:

1. Correctness:
   Evaluate whether the technical information is correct.

2. Relevance:
   Evaluate whether the candidate directly answers the question.

3. Completeness:
   Evaluate whether the answer covers the important concepts required
   to answer the question adequately.

4. Clarity:
   Evaluate whether the explanation is understandable, structured,
   and sufficiently clear.

Scoring:

- Give each criterion a score from 0 to 10.
- 0 means the criterion is completely unsatisfied.
- 10 means the criterion is fully satisfied.
- Evaluate the actual answer provided.
- Do not give a high score simply because the answer sounds confident.
- Do not penalize an answer for minor wording or grammar issues if the
  technical meaning is clear.
- Do not invent information that is not present in the candidate's answer.

Provide:

- strengths
- weaknesses
- specific improvement feedback

Interview Question:
{question_text}

Candidate Answer:
{answer_text}
""".strip()
