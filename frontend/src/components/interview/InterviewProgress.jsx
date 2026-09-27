function InterviewProgress({
  questionNumber,
  totalQuestions,
  interviewId,
}) {
  return (
    <div className="mb-6 flex items-center justify-between">
      <span className="text-sm font-medium text-gray-600">
        Question {questionNumber} of {totalQuestions}
      </span>

      <span className="text-sm text-gray-500">
        Interview #{interviewId}
      </span>
    </div>
  );
}

export default InterviewProgress;