function InterviewHeader({ interviewType }) {
  return (
    <div className="mb-8">
      <h1 className="text-3xl font-bold">
        AI Interview
      </h1>

      <p className="mt-2 text-gray-600">
        {interviewType}
      </p>
    </div>
  );
}

export default InterviewHeader;