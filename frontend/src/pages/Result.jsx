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

        const data = await getInterviewResult(id);

        setResult(data);
      } catch (err) {
        console.error("Failed to load interview result:", err);

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

    if (id) {
      fetchResult();
    } else {
      setLoading(false);
      setError("Invalid interview ID.");
    }
  }, [id]);

  if (loading) {
    return (
      <div className="mx-auto max-w-3xl px-6 py-10">
        <div className="rounded-xl border bg-white p-8 shadow-sm">
          <p className="text-gray-600">
            Loading interview result...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-3xl px-6 py-10">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6">
          <h2 className="text-lg font-semibold text-red-800">
            Unable to load result
          </h2>

          <p className="mt-2 text-sm text-red-700">
            {error}
          </p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="mx-auto max-w-3xl px-6 py-10">
        <div className="rounded-xl border bg-white p-8 shadow-sm">
          <h2 className="text-lg font-semibold">
            Result Not Found
          </h2>

          <p className="mt-2 text-gray-600">
            No interview result was found for this interview.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">
          Interview Result
        </h1>

        <p className="mt-2 text-gray-600">
          Here is a summary of your interview.
        </p>
      </div>

      <InterviewSummary result={result} />
    </div>
  );
}

export default Result;