import { formatDuration } from "../../utils/formatDuration";

function InterviewSummary({ result }) {
  return (
    <div className="space-y-6">
      {/* Shows the main interview information. */}
      <div className="rounded-xl border bg-white p-8 shadow-sm">
        <div>
          <h2 className="text-xl font-semibold">
            Interview Summary
          </h2>

          <p className="mt-1 text-sm text-gray-500">
            Your interview has been completed.
          </p>
        </div>

        {/* Keeps summary information easy to scan. */}
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
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

          {/* Overall score is calculated by the backend. */}
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

      {/* Main AI evaluation section. */}
      <div className="rounded-xl border bg-white p-8 shadow-sm">
        <div>
          <h2 className="text-xl font-semibold">
            AI Evaluation
          </h2>

          <p className="mt-1 text-sm text-gray-500">
            Review your answers and AI feedback.
          </p>
        </div>

        {/* 
          Questions are placed in one horizontal row.
          The scrollbar is hidden to keep the UI clean.
        */}
        <div className="hide-scrollbar mt-6 flex snap-x snap-mandatory gap-5 overflow-x-auto pb-2">
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

        {/* Small hint so users know the cards can be moved. */}
        {result.evaluations?.length > 1 && (
          <p className="mt-4 text-center text-xs text-gray-400">
            Scroll horizontally to view other questions
          </p>
        )}
      </div>
    </div>
  );
}

/*
 * One question becomes one horizontal card.
 */
function EvaluationItem({ item, questionNumber }) {
  const evaluation = item.evaluation;

  return (
    <div
      className="
        min-w-[88%]
        snap-start
        rounded-xl
        border
        bg-gray-50
        p-6
        sm:min-w-[75%]
        lg:min-w-[65%]
        xl:min-w-[55%]
      "
    >
      {/* Question number. */}
      <h3 className="text-lg font-semibold text-gray-900">
        Question {questionNumber}
      </h3>

      {/* Interview question. */}
      <p className="mt-3 leading-7 text-gray-800">
        {item.question_text || "Question not available."}
      </p>

      {/* Candidate answer. */}
      <div className="mt-5 rounded-lg bg-white p-4">
        <p className="text-sm font-medium text-gray-500">
          Your Answer
        </p>

        <p className="mt-2 whitespace-pre-wrap leading-7 text-gray-800">
          {item.answer_text || "No answer available."}
        </p>
      </div>

      {/* Show evaluation when available. */}
      {evaluation ? (
        <>
          {/* Four main AI scores. */}
          <div className="mt-5 grid grid-cols-2 gap-3">
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

          {/* Score for this answer. */}
          <div className="mt-4 rounded-lg border bg-white p-4">
            <p className="text-sm text-gray-500">
              Answer Score
            </p>

            <p className="mt-1 text-xl font-semibold text-gray-900">
              {evaluation.overall_score} / 10
            </p>
          </div>

          {/* AI feedback. */}
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
        <p className="mt-5 text-sm text-gray-500">
          AI evaluation is not available for this answer.
        </p>
      )}
    </div>
  );
}

/* Shows one evaluation score. */
function ScoreItem({ label, score }) {
  return (
    <div className="rounded-lg bg-white p-4">
      <p className="text-sm text-gray-500">
        {label}
      </p>

      <p className="mt-1 text-lg font-semibold text-gray-900">
        {score} / 10
      </p>
    </div>
  );
}

/* Shows one feedback section. */
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

/* Reusable summary field. */
function SummaryItem({ label, value }) {
  return (
    <div className="rounded-lg bg-gray-50 p-4">
      <p className="text-sm text-gray-500">
        {label}
      </p>

      <p className="mt-1 text-lg font-medium text-gray-900">
        {value}
      </p>
    </div>
  );
}

export default InterviewSummary;