import { useState } from "react";
import {
  useLocation,
  useNavigate,
  useParams,
} from "react-router-dom";

import { submitAnswer } from "../services/api/answerApi";

function Interview() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const [interview, setInterview] = useState(location.state);
  const [answer, setAnswer] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  if (!interview) {
    return (
      <div className="mx-auto max-w-3xl px-6 py-10">
        <div className="rounded-xl border bg-white p-6 shadow-sm">
          <h1 className="text-xl font-semibold">
            Interview data not found
          </h1>

          <p className="mt-2 text-gray-600">
            Please start the interview again from the resume page.
          </p>
        </div>
      </div>
    );
  }

  const handleSubmitAnswer = async () => {
    if (!answer.trim()) {
      setError("Please enter an answer before submitting.");
      return;
    }

    try {
      setSubmitting(true);
      setError("");

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

      setInterview({
        ...interview,
        question_id: data.next_question_id,
        question_number: data.next_question_number,
        question_text: data.next_question_text,
      });
    } catch (err) {
      console.error("Answer submission error:", err);

      const detail = err.response?.data?.detail;

      if (Array.isArray(detail)) {
        setError(
          detail
            .map((item) => item.msg)
            .filter(Boolean)
            .join(", ")
        );
      } else if (typeof detail === "string") {
        setError(detail);
      } else {
        setError("Failed to submit answer.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold">
          AI Interview
        </h1>

        <p className="mt-2 text-gray-600">
          {interview.interview_type}
        </p>
      </div>

      {/* Progress */}
      <div className="mb-6 flex items-center justify-between">
        <span className="text-sm font-medium text-gray-600">
          Question {interview.question_number} of{" "}
          {interview.total_questions}
        </span>

        <span className="text-sm text-gray-500">
          Interview #{id}
        </span>
      </div>

      {/* Question */}
      <div className="rounded-xl border bg-white p-8 shadow-sm">
        <h2 className="text-xl font-semibold">
          Question {interview.question_number}
        </h2>

        <p className="mt-6 text-lg leading-8 text-gray-800">
          {interview.question_text}
        </p>

        {/* Answer */}
        <div className="mt-8">
          <label
            htmlFor="answer"
            className="block text-sm font-medium text-gray-700"
          >
            Your Answer
          </label>

          <textarea
            id="answer"
            rows="8"
            value={answer}
            onChange={(event) => setAnswer(event.target.value)}
            placeholder="Type your answer here..."
            disabled={submitting}
            className="mt-2 block w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
          />

          {error && (
            <p className="mt-3 text-sm text-red-600">
              {error}
            </p>
          )}

          <button
            type="button"
            onClick={handleSubmitAnswer}
            disabled={submitting}
            className="mt-5 rounded-lg bg-blue-600 px-6 py-3 font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {submitting ? "Submitting..." : "Submit Answer"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Interview;