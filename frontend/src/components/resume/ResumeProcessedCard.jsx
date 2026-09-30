function ResumeProcessedCard({
  candidate,
  onStartInterview,
}) {
  /*
   * Do not render anything until a candidate
   * has been successfully created.
   */
  if (!candidate) {
    return null;
  }

  return (
    <div className="mt-8 rounded-xl border bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold">
        Resume Processed
      </h2>

      <div className="mt-4 space-y-2">
        <p>
          <strong>Name:</strong> {candidate.name}
        </p>

        <p>
          <strong>Email:</strong> {candidate.email}
        </p>

        <p>
          <strong>Resume:</strong>{" "}
          {candidate.resume_filename}
        </p>

        <p>
          <strong>Interview Type:</strong>{" "}
          {candidate.interview_type}
        </p>

        <p>
          <strong>Candidate ID:</strong>{" "}
          {candidate.id}
        </p>
      </div>

      <button
        type="button"
        onClick={onStartInterview}
        className="mt-6 rounded-lg bg-green-600 px-5 py-2.5 font-medium text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        Configure Interview
      </button>
    </div>
  );
}

export default ResumeProcessedCard;