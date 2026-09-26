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