function InterviewSummary({ result }) {
  return (
    <div className="rounded-xl border bg-white p-8 shadow-sm">
      <h2 className="text-xl font-semibold">
        Interview Summary
      </h2>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <SummaryItem
          label="Interview ID"
          value={result.interview_id}
        />

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
          value={`${result.duration_seconds} seconds`}
        />
      </div>
    </div>
  );
}

function SummaryItem({ label, value }) {
  return (
    <div>
      <p className="text-sm text-gray-500">
        {label}
      </p>

      <p className="mt-1 font-medium">
        {value}
      </p>
    </div>
  );
}

export default InterviewSummary;