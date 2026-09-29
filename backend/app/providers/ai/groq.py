from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.providers.ai.base import AIProvider
from app.core.config import settings
from app.schemas.ai_evaluation import AIEvaluationResponse


class GroqProvider(AIProvider):

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ):

        self.api_key = api_key or settings.GROQ_API_KEY

        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not configured.")

        self.model = model or settings.GROQ_MODEL

        if not self.model:
            raise ValueError("GROQ_MODEL environment variable is not configured.")

        self.llm = ChatGroq(api_key=self.api_key, model=self.model, temperature=0)

        self.structured_llm = self.llm.with_structured_output(AIEvaluationResponse)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """ 
You are an expert technical interviewer.

Evaluate the candidate's answer against the interview question.

Evaluate the answer using these four criteria:

1. Correctness
   - Is the technical information correct?

2. Relevance
   - Does the answer directly address the question?

3. Completeness
   - Does the answer cover the important concepts required?

4. Clarity
   - Is the explanation clear and understandable?

Scoring rules:

- Give each criterion a score from 0 to 10.
- 0 means the criterion is completely unsatisfied.
- 10 means the criterion is fully satisfied.
- Evaluate only the information present in the candidate's answer.
- Do not invent information.
- Do not calculate an overall score.
- Provide specific and useful feedback.

Return the evaluation using the required structured format.

""",
                ),
                (
                    "human",
                    """ 
Interview Question:
{question_text}

Candidate Answer:
{answer_text}
""",
                ),
            ]
        )

        self.chain = self.prompt | self.structured_llm

    def evaluate_answer(
        self,
        question_text: str,
        answer_text: str,
    ) -> AIEvaluationResponse:

        if not question_text.strip():
            raise ValueError("Question text cannot be empty.")

        if not answer_text.strip():
            raise ValueError("Candidate answer cannot be empty.")

        try:
            result = self.chain.invoke(
                {
                    "question_text": question_text,
                    "answer_text": answer_text,
                }
            )

            if not isinstance(result, AIEvaluationResponse):
                raise ValueError("Groq returned an invalid evaluation response.")

            return result

        except Exception as exc:
            raise RuntimeError(
                "Failed to evaluate the candidate's answer using Groq."
            ) from exc
