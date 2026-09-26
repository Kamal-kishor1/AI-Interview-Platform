import api from "./axios";

export const getInterviewResult = async (interviewId) => {
  const response = await api.get(
    `/api/v1/interviews/${interviewId}/result`
  );

  return response.data;
};