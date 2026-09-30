from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.providers.ai.base import AIProvider

from app.core.config import settings

from app.schemas.ai_evaluation import AIEvaluationResponse
from app.schemas.candidate_context import CandidateContextExtraction


class GroqProvider(AIProvider):

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ):

        # Groq configuration

        self.api_key = api_key or settings.GROQ_API_KEY

        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not configured.")

        self.model = model or settings.GROQ_MODEL

        if not self.model:
            raise ValueError("GROQ_MODEL environment variable is not configured.")

        # base groq llm

        self.llm = ChatGroq(api_key=self.api_key, model=self.model, temperature=0)

        # ai evaluation

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

        # candidate context extraction

        self.candidate_context_llm = self.llm.with_structured_output(
            CandidateContextExtraction
        )

        # prompt specifically for resume extraction

        self.extract_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a professional resume information extractor.

Your task is to extract structured candidate information
from the provided resume text.

Extract ONLY information that is explicitly present in
the resume.

Do NOT:
- invent information
- infer skills that are not stated
- create projects that are not present
- create work experience that is not present
- add technologies that are not explicitly supported
- add assumptions about the candidate

Extract these three categories:

1. Skills
   - Extract technical and professional skills explicitly
     mentioned in the resume.
   - Return each skill as a separate item.

2. Projects
   - Extract projects explicitly mentioned in the resume.
   - For each project provide:
     - project name
     - description when available
     - technologies explicitly mentioned for that project

3. Experience
   - Extract work experience, internships, or other
     professional experience explicitly mentioned.
   - For each experience provide:
     - role when available
     - company when available
     - description when available

If a category is not present in the resume, return an
empty list for that category.

The output must follow the provided structured schema.
""",
                ),
                (
                    "human",
                    """
Resume Text:

{resume_text}
""",
                ),
            ]
        )

        # this is chain which works: resume text -> extraction prompt -> groq llm -> response schema

        self.extract_chain = self.extract_prompt | self.candidate_context_llm

    # ai evaluation

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

    # candidate context extraction

    async def extract_candidate_context(
        self, resume_text: str
    ) -> CandidateContextExtraction:

        if not resume_text or not resume_text.strip():
            raise ValueError("Resume text can not be empty.")

        try:

            result = await self.extract_chain.ainvoke({"resume_text": resume_text})

            # validate returned object

            if not isinstance(result, CandidateContextExtraction):
                raise ValueError("Groq returned an invalid evaluation response.")

            return result

        except Exception as exc:
            raise RuntimeError(
                "Failed to evaluate the candidate's answer using Groq."
            ) from exc
