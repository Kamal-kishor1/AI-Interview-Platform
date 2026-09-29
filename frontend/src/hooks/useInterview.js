import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { submitAnswer } from "../services/api/answerApi";
import { getCurrentQuestion } from "../services/api/interviewApi";

import { getApiErrorMessage } from "../utils/errorHandler";

function useInterview(interviewId) {
  const navigate = useNavigate();

  // Stores the current interview/question data.
  const [interview, setInterview] = useState(null);

  // Stores the candidate's current answer.
  const [answer, setAnswer] = useState("");

  // Stores the AI evaluation returned after submitting an answer.
  // This is mainly useful if the interview UI needs to access
  // the evaluation before navigating to the result page.
  const [evaluation, setEvaluation] = useState(null);

  // Loading state while the current question is being fetched.
  const [loading, setLoading] = useState(true);

  // Loading state while an answer is being submitted.
  const [submitting, setSubmitting] = useState(false);

  // Error shown when the interview/question cannot be loaded.
  const [loadError, setLoadError] = useState("");

  // Error shown when the answer cannot be submitted.
  const [submitError, setSubmitError] = useState("");

  /*
   * Load the current interview question when the interview ID changes.
   */
  useEffect(() => {
    const fetchCurrentQuestion = async () => {
      try {
        setLoading(true);
        setLoadError("");

        const data = await getCurrentQuestion(interviewId);

        console.log("Current interview question:", data);

        // Store the current interview/question information.
        setInterview(data);
      } catch (err) {
        console.error("Failed to load interview:", err);

        // Convert backend/API errors into a user-friendly message.
        setLoadError(
          getApiErrorMessage(
            err,
            "Failed to load interview."
          )
        );
      } finally {
        setLoading(false);
      }
    };

    // Only request the interview if a valid ID exists.
    if (interviewId) {
      fetchCurrentQuestion();
    } else {
      setLoading(false);
      setLoadError("Invalid interview ID.");
    }
  }, [interviewId]);

  /*
   * Submit the candidate's current answer.
   */
  const handleSubmitAnswer = async () => {
    // Make sure interview data has been loaded.
    if (!interview) {
      setSubmitError("Interview data is not available.");
      return;
    }

    // Prevent empty answers from being submitted.
    if (!answer.trim()) {
      setSubmitError(
        "Please enter an answer before submitting."
      );
      return;
    }

    try {
      setSubmitting(true);
      setSubmitError("");

      /*
       * Send the current answer to the backend.
       *
       * The backend now:
       * 1. Saves the answer.
       * 2. Evaluates it using Groq.
       * 3. Saves the evaluation.
       * 4. Returns the evaluation and next question.
       */
      const data = await submitAnswer(
        interview.interview_id,
        interview.question_id,
        answer
      );

      console.log("Answer submitted:", data);

      // Clear the answer input after successful submission.
      setAnswer("");

      /*
       * Store the AI evaluation returned by the backend.
       *
       * data.evaluation contains:
       * - correctness_score
       * - relevance_score
       * - completeness_score
       * - clarity_score
       * - overall_score
       * - strengths
       * - weaknesses
       * - improvement_feedback
       */
      setEvaluation(data.evaluation);

      /*
       * If this was the final question, go to the result page.
       *
       * The result page should later fetch the complete interview
       * result from the backend using interview_id.
       */
      if (data.interview_completed) {
        navigate(`/result/${data.interview_id}`);
        return;
      }

      /*
       * Update the interview state with the next question.
       *
       * We keep the existing interview information and replace
       * only the question-related fields.
       */
      setInterview((current) => ({
        ...current,
        question_id: data.next_question_id,
        question_number: data.next_question_number,
        question_text: data.next_question_text,
      }));
    } catch (err) {
      console.error("Answer submission error:", err);

      // Convert API/backend errors into a user-friendly message.
      setSubmitError(
        getApiErrorMessage(
          err,
          "Failed to submit answer."
        )
      );
    } finally {
      // Allow the user to submit again after the request finishes.
      setSubmitting(false);
    }
  };

  /*
   * Expose the state and actions required by Interview.jsx.
   */
  return {
    interview,
    answer,
    setAnswer,

    evaluation,
    setEvaluation,

    loading,
    submitting,

    loadError,
    submitError,

    handleSubmitAnswer,
  };
}

export default useInterview;