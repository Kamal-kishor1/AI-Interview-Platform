import api from "./axios";

export const startInterview = async (candidateId) => {
  const response = await api.post(
    "/api/v1/interviews/start",
    {
      candidate_id: candidateId,
    }
  );

  return response.data;
};

export const getCurrentQuestion = async (interviewId) => {
  const response = await api.get(
    `/api/v1/interviews/${interviewId}/current-question`
  );

  return response.data;
};