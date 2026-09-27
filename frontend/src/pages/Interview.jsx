import { useParams } from "react-router-dom";

import useInterview from "../hooks/useInterview";

import AnswerForm from "../components/interview/AnswerForm";
import InterviewHeader from "../components/interview/InterviewHeader";
import InterviewProgress from "../components/interview/InterviewProgress";
import InterviewQuestion from "../components/interview/InterviewQuestion";

function Interview() {
  const { id } = useParams();

  const {
    interview,
    answer,
    setAnswer,
    loading,
    submitting,
    loadError,
    submitError,
    handleSubmitAnswer,
  } = useInterview(id);

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-6 py-10">
        <p className="text-gray-600">
          Loading interview...
        </p>
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="mx-auto max-w-4xl px-6 py-10">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6">
          <h1 className="text-xl font-semibold text-red-700">
            Unable to load interview
          </h1>

          <p className="mt-2 text-red-600">
            {loadError}
          </p>
        </div>
      </div>
    );
  }

  if (!interview) {
    return (
      <div className="mx-auto max-w-4xl px-6 py-10">
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

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">

      <InterviewHeader
        interviewType={interview.interview_type}
      />

      <InterviewProgress
        questionNumber={interview.question_number}
        totalQuestions={interview.total_questions}
        interviewId={interview.interview_id}
      />

      <InterviewQuestion
        questionNumber={interview.question_number}
        questionText={interview.question_text}
      >
        <AnswerForm
          answer={answer}
          setAnswer={setAnswer}
          submitting={submitting}
          submitError={submitError}
          onSubmit={handleSubmitAnswer}
        />
      </InterviewQuestion>

    </div>
  );
}

export default Interview;