import { formatDuration } from "../../utils/formatDuration";

function InterviewSummary({ result }) {
  return (
    <div className="space-y-6">
      {/* This card shows the basic interview information. */}
      <div className="rounded-xl border bg-white p-8 shadow-sm">
        <div>
          <h2 className="text-xl font-semibold">Interview Summary</h2>

          <p className="mt-1 text-sm text-gray-500">
            Your interview has been completed.
          </p>
        </div>

        {/* Show important interview details in a simple grid. */}
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <SummaryItem
            label="Candidate Name"
            value={result.candidate_name}
          />

          <SummaryItem
            label="Interview Type"
            value={result.interview_type}
          />

          <SummaryItem
            label="Status"
            value={result.status}
          />

          <SummaryItem
            label="Questions"
            value={`${result.answered_questions} / ${result.total_questions}`}
          />

          <SummaryItem
            label="Completion"
            value={`${result.completion_percentage}%`}
          />

          <SummaryItem
            label="Duration"
            value={formatDuration(result.duration_seconds)}
          />

          {/* Overall score comes from the backend calculation. */}
          <SummaryItem
            label="Overall Score"
            value={
              result.overall_score !== null &&
              result.overall_score !== undefined
                ? `${result.overall_score} / 10`
                : "N/A"
            }
          />
        </div>
      </div>

      {/* Show the AI evaluation for every submitted answer. */}
      <div className="rounded-xl border bg-white p-8 shadow-sm">
        <div>
          <h2 className="text-xl font-semibold">
            AI Evaluation
          </h2>

          <p className="mt-1 text-sm text-gray-500">
            Review your answers and AI feedback.
          </p>
        </div>

        <div className="mt-6 space-y-6">
          {/* evaluations is an array because an interview has many answers. */}
          {result.evaluations?.length > 0 ? (
            result.evaluations.map((item, index) => (
              <EvaluationItem
                key={item.answer_id}
                item={item}
                questionNumber={index + 1}
              />
            ))
          ) : (
            <p className="text-sm text-gray-500">
              No evaluations are available.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

/*
 * Displays one question, the candidate's answer,
 * and its AI evaluation.
 */
function EvaluationItem({ item, questionNumber }) {
  const evaluation = item.evaluation;

  return (
    <div className="rounded-xl border bg-gray-50 p-6">
      {/* Question */}
      <h3 className="text-lg font-semibold text-gray-900">
        Question {questionNumber}
      </h3>

      <p className="mt-3 leading-7 text-gray-800">
        {item.question_text || "Question not available."}
      </p>

      {/* Candidate answer */}
      <div className="mt-5">
        <p className="text-sm font-medium text-gray-500">
          Your Answer
        </p>

        <p className="mt-2 whitespace-pre-wrap leading-7 text-gray-800">
          {item.answer_text || "No answer available."}
        </p>
      </div>

      {/* Evaluation may be missing, so handle that safely. */}
      {evaluation ? (
        <>
          {/* Four individual AI scores. */}
          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            <ScoreItem
              label="Correctness"
              score={evaluation.correctness_score}
            />

            <ScoreItem
              label="Relevance"
              score={evaluation.relevance_score}
            />

            <ScoreItem
              label="Completeness"
              score={evaluation.completeness_score}
            />

            <ScoreItem
              label="Clarity"
              score={evaluation.clarity_score}
            />
          </div>

          {/* Overall score for this particular answer. */}
          <div className="mt-4 rounded-lg border bg-white p-4">
            <p className="text-sm text-gray-500">
              Answer Score
            </p>

            <p className="mt-1 text-xl font-semibold text-gray-900">
              {evaluation.overall_score} / 10
            </p>
          </div>

          {/* AI feedback sections. */}
          <FeedbackItem
            title="Strengths"
            content={evaluation.strengths}
          />

          <FeedbackItem
            title="Weaknesses"
            content={evaluation.weaknesses}
          />

          <FeedbackItem
            title="Improvement Feedback"
            content={evaluation.improvement_feedback}
          />
        </>
      ) : (
        <p className="mt-6 text-sm text-gray-500">
          AI evaluation is not available for this answer.
        </p>
      )}
    </div>
  );
}

/* Displays one score such as Correctness: 8/10. */
function ScoreItem({ label, score }) {
  return (
    <div className="rounded-lg bg-white p-4">
      <p className="text-sm text-gray-500">{label}</p>

      <p className="mt-1 text-lg font-semibold text-gray-900">
        {score} / 10
      </p>
    </div>
  );
}

/* Displays one feedback section. */
function FeedbackItem({ title, content }) {
  return (
    <div className="mt-5 rounded-lg bg-white p-4">
      <p className="text-sm font-medium text-gray-500">
        {title}
      </p>

      <p className="mt-2 whitespace-pre-wrap leading-7 text-gray-800">
        {content || "No feedback available."}
      </p>
    </div>
  );
}

/* Reusable component for basic interview information. */
function SummaryItem({ label, value }) {
  return (
    <div className="rounded-lg bg-gray-50 p-4">
      <p className="text-sm text-gray-500">{label}</p>

      <p className="mt-1 text-lg font-medium text-gray-900">
        {value}
      </p>
    </div>
  );
}

export default InterviewSummary;