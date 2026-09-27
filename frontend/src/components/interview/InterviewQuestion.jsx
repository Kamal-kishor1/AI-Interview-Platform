function InterviewQuestion({
  questionNumber,
  questionText,
  children,
}) {
  return (
    <div className="rounded-xl border bg-white p-8 shadow-sm">

      <h2 className="text-xl font-semibold">
        Question {questionNumber}
      </h2>

      <p className="mt-6 text-lg leading-8 text-gray-800">
        {questionText}
      </p>

      {children}

    </div>
  );
}

export default InterviewQuestion;