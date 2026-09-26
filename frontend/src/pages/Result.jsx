import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getInterviewResult } from "../services/api/resultApi";

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

        console.log("Interview result:", data);

        setResult(data);
      } catch (err) {
        console.error("Result fetch error:", err);

        const detail = err.response?.data?.detail;

        setError(
          typeof detail === "string"
            ? detail
            : "Failed to load interview result."
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
    return null;
  }

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold">
          Interview Completed
        </h1>

        <p className="mt-2 text-gray-600">
          Your interview has been successfully completed.
        </p>
      </div>

      <div className="rounded-xl border bg-white p-8 shadow-sm">
        <h2 className="text-xl font-semibold">
          Interview Summary
        </h2>

        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <div>
            <p className="text-sm text-gray-500">
              Interview ID
            </p>
            <p className="mt-1 font-medium">
              {result.interview_id}
            </p>
          </div>

          <div>
            <p className="text-sm text-gray-500">
              Candidate Name
            </p>
            <p className="mt-1 font-medium">
              {result.candidate_name}
            </p>
          </div>

          <div>
            <p className="text-sm text-gray-500">
              Interview Type
            </p>
            <p className="mt-1 font-medium">
              {result.interview_type}
            </p>
          </div>

          <div>
            <p className="text-sm text-gray-500">
              Status
            </p>
            <p className="mt-1 font-medium">
              {result.status}
            </p>
          </div>

          <div>
            <p className="text-sm text-gray-500">
              Questions
            </p>
            <p className="mt-1 font-medium">
              {result.answered_questions} /{" "}
              {result.total_questions}
            </p>
          </div>

          <div>
            <p className="text-sm text-gray-500">
              Completion
            </p>
            <p className="mt-1 font-medium">
              {result.completion_percentage}%
            </p>
          </div>

          <div>
            <p className="text-sm text-gray-500">
              Duration
            </p>
            <p className="mt-1 font-medium">
              {result.duration_seconds} seconds
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Result;