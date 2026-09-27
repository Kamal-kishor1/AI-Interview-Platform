import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import InterviewSummary from "../components/result/InterviewSummary";

import { getInterviewResult } from "../services/api/resultApi";
import { getApiErrorMessage } from "../utils/errorHandler";

function Result() {
  const { id } = useParams();

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchResult = async () => {
      try {
        setLoading(true);
        setError("");

        const resultData =
          await getInterviewResult(id);

        console.log(
          "Interview result:",
          resultData
        );

        setResult(resultData);
      } catch (err) {
        console.error(
          "Result fetch error:",
          err
        );

        setError(
          getApiErrorMessage(
            err,
            "Failed to load interview result."
          )
        );
      } finally {
        setLoading(false);
      }
    };

    fetchResult();
  }, [id]);

  if (loading) {
    return (
      <div className="mx-auto max-w-3xl px-6 py-10">
        <p className="text-gray-600">
          Loading interview result...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-3xl px-6 py-10">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6">
          <h1 className="text-xl font-semibold text-red-700">
            Unable to load result
          </h1>

          <p className="mt-2 text-red-600">
            {error}
          </p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="mx-auto max-w-3xl px-6 py-10">
        <p className="text-gray-600">
          Interview result not found.
        </p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      {/* Header */}
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold">
          Interview Completed
        </h1>

        <p className="mt-2 text-gray-600">
          Your interview has been successfully
          completed.
        </p>
      </div>

      {/* Summary */}
      <InterviewSummary result={result} />
    </div>
  );
}

export default Result;