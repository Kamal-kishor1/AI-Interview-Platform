import api from "./axios";

export const getCandidate = async (candidateId) => {
  const response = await api.get(
    `/api/v1/candidates/${candidateId}`
  );

  return response.data;
};