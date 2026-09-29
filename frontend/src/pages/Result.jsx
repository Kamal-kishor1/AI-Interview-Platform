import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import InterviewSummary from "../components/result/InterviewSummary";
import { getInterviewResult } from "../services/api/resultApi";
import { getApiErrorMessage } from "../utils/errorHandler";

function Result() {
  // Get the interview ID from /result/:id.
  const { id } = useParams();

  // Stores the complete result returned by the backend.
  const [result, setResult] = useState(null);

  // Controls the loading UI while the API request is running.
  const [loading, setLoading] = useState(true);

  // Stores a user-friendly API error.
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchResult = async () => {
      try {
        setLoading(true);
        setError("");

        // Clear old result data when loading another interview.
        setResult(null);

        // Fetch the complete interview result from the backend.
        const data = await getInterviewResult(id);

        // Store the result so InterviewSummary can display it.
        setResult(data);
      } catch (err) {
        console.error(
          "Failed to load interview result:",
          err
        );

        // Convert backend errors into a readable message.
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

    // Only call the API when an interview ID exists.
    if (id) {
      fetchResult();
    } else {
      setLoading(false);
      setError("Invalid interview ID.");
    }
  }, [id]);

  // Show loading state while fetching the result.
  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-6 py-10">
        <div className="rounded-xl border bg-white p-8 shadow-sm">
          <p className="text-gray-600">
            Loading interview result...
          </p>
        </div>
      </div>
    );
  }

  // Show API/server errors.
  if (error) {
    return (
      <div className="mx-auto max-w-4xl px-6 py-10">
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

  // Handle a successful request that returned no result.
  if (!result) {
    return (
      <div className="mx-auto max-w-4xl px-6 py-10">
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

  // Display the complete interview result.
  return (
    <div className="mx-auto max-w-6xl px-6 py-10">
      {/* Page heading. */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold">
          Interview Result
        </h1>

        <p className="mt-2 text-gray-600">
          Here is a summary of your interview and AI feedback.
        </p>
      </div>

      {/* Keep result presentation inside InterviewSummary. */}
      <InterviewSummary result={result} />
    </div>
  );
}

export default Result;