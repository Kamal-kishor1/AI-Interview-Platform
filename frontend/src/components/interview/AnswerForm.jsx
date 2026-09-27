function AnswerForm({
  answer,
  setAnswer,
  submitting,
  submitError,
  onSubmit,
}) {
  return (
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
        onChange={(event) => {
          setAnswer(event.target.value);
        }}
        placeholder="Type your answer here..."
        disabled={submitting}
        className="mt-2 block w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
      />

      {submitError && (
        <p className="mt-3 text-sm text-red-600">
          {submitError}
        </p>
      )}

      <button
        type="button"
        onClick={onSubmit}
        disabled={submitting}
        className="mt-5 rounded-lg bg-blue-600 px-6 py-3 font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {submitting ? "Submitting..." : "Submit Answer"}
      </button>

    </div>
  );
}

export default AnswerForm;