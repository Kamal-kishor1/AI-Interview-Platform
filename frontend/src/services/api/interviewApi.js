import api from "./axios";

/*
 * Start an interview using the complete
 * interview configuration.
 *
 * @param {Object} interviewData
 * @returns {Object} interview response
 */

export const startInterview = async (interviewData) => {
  const response = await api.post(
    "/api/v1/interviews/start",
    interviewData
  );

  return response.data;
};

/*
 * Get the current unanswered question
 * for an existing interview.
 */
export const getCurrentQuestion = async (interviewId) => {
  const response = await api.get(
    `/api/v1/interviews/${interviewId}/current-question`
  );

  return response.data;
};