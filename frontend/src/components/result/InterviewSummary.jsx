import { formatDuration } from "../../utils/formatDuration";

function InterviewSummary({ result }) {
  return (
    <div className="rounded-xl border bg-white p-8 shadow-sm">
      <div>
        <h2 className="text-xl font-semibold">Interview Summary</h2>

        <p className="mt-1 text-sm text-gray-500">
          Your interview has been completed.
        </p>
      </div>

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
      </div>
    </div>
  );
}

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