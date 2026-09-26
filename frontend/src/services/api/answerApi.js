import api from "./axios";

export const submitAnswer = async (
  interviewId,
  questionId,
  answerText
) => {
  const response = await api.post(
    `/api/v1/interviews/${interviewId}/answers`,
    {
      question_id: questionId,
      answer_text: answerText,
    }
  );

  return response.data;
};