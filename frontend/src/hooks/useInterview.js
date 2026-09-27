import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { submitAnswer } from "../services/api/answerApi";
import { getCurrentQuestion } from "../services/api/interviewApi";

import { getApiErrorMessage } from "../utils/errorHandler";

function useInterview(interviewId) {
  const navigate = useNavigate();

  const [interview, setInterview] = useState(null);
  const [answer, setAnswer] = useState("");

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const [loadError, setLoadError] = useState("");
  const [submitError, setSubmitError] = useState("");

  useEffect(() => {
    const fetchCurrentQuestion = async () => {
      try {
        setLoading(true);
        setLoadError("");

        const data = await getCurrentQuestion(interviewId);

        console.log("Current interview question:", data);

        setInterview(data);
      } catch (err) {
        console.error("Failed to load interview:", err);

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

    if (interviewId) {
      fetchCurrentQuestion();
    } else {
      setLoading(false);
      setLoadError("Invalid interview ID.");
    }
  }, [interviewId]);

  const handleSubmitAnswer = async () => {
    if (!interview) {
      setSubmitError("Interview data is not available.");
      return;
    }

    if (!answer.trim()) {
      setSubmitError(
        "Please enter an answer before submitting."
      );
      return;
    }

    try {
      setSubmitting(true);
      setSubmitError("");

      const data = await submitAnswer(
        interview.interview_id,
        interview.question_id,
        answer
      );

      console.log("Answer submitted:", data);

      setAnswer("");

      if (data.interview_completed) {
        navigate(`/result/${data.interview_id}`);
        return;
      }

      setInterview((current) => ({
        ...current,
        question_id: data.next_question_id,
        question_number: data.next_question_number,
        question_text: data.next_question_text,
      }));
    } catch (err) {
      console.error("Answer submission error:", err);

      setSubmitError(
        getApiErrorMessage(
          err,
          "Failed to submit answer."
        )
      );
    } finally {
      setSubmitting(false);
    }
  };

  return {
    interview,
    answer,
    setAnswer,
    loading,
    submitting,
    loadError,
    submitError,
    handleSubmitAnswer,
  };
}

export default useInterview;