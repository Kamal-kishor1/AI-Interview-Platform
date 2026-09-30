import { useEffect, useState } from "react";

import {
    useNavigate,
    useParams,
} from "react-router-dom";

import { getCandidate } from "../services/api/candidateApi";
import { startInterview } from "../services/api/interviewApi";
import { getApiErrorMessage } from "../utils/errorHandler";


function InterviewConfiguration() {
  const navigate = useNavigate();
  const { candidateId } = useParams();

  /*
   * Interview configuration defaults.
   */
  const [difficulty, setDifficulty] =
    useState("MEDIUM");

  const [questionCount, setQuestionCount] =
    useState(10);

  /*
   * Personalization options.
   *
   * All are enabled by default according
   * to the Phase 6.1 configuration.
   */
  const [useSkills, setUseSkills] =
    useState(true);

  const [useProjects, setUseProjects] =
    useState(true);

  const [useExperience, setUseExperience] =
    useState(true);

  const [useResume, setUseResume] =
    useState(true);

  const [startingInterview, setStartingInterview] =
    useState(false);

  const [error, setError] = useState("");

  /* Read candidate from url */

  const [candidate, setCandidate] = useState(null);
  const [loading, setLoadingCandidate] = useState(false);

  useEffect(() => {
    const loadCandidate = async () => {
        try {
            setLoadingCandidate(true);

            const data = await getCandidate(candidateId);
            setCandidate(data);
        } catch (err) {
            setError(
                getApiErrorMessage(
                    err,
                    "Failed to load candidate."
                )
            );
        } finally{
            setLoadingCandidate(false);
        }
    };
    loadCandidate();
  }, [candidateId]);

  /*
   * Handle configuration submission.
   */
  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    /*
     * Frontend validation.
     *
     * The backend remains the final authority
     * for validation.
     */
    if (
      questionCount < 5 ||
      questionCount > 30
    ) {
      setError(
        "Question count must be between 5 and 30."
      );
      return;
    }

    /*
     * At least one personalization source
     * must be selected.
     */
    if (
      !useSkills &&
      !useProjects &&
      !useExperience &&
      !useResume
    ) {
      setError(
        "Select at least one personalization source."
      );
      return;
    }

    /*
     * Build the request payload expected
     * by the backend.
     */
    const interviewConfiguration = {
      candidate_id: Number(candidateId),
      difficulty,
      question_count: questionCount,
      use_skills: useSkills,
      use_projects: useProjects,
      use_experience: useExperience,
      use_resume: useResume,
    };

    try {
      setStartingInterview(true);

      console.log(
        "Starting interview with configuration:",
        interviewConfiguration
      );

      /*
       * Call the backend.
       */
      const interviewData =
        await startInterview(
          interviewConfiguration
        );

      console.log(
        "Interview started:",
        interviewData
      );

      /*
       * Navigate to the actual interview page
       * after successful API response.
       */
      navigate(
        `/interview/${interviewData.interview_id}`,
        {
          state: interviewData,
        }
      );
    } catch (err) {
      console.error(
        "Start interview error:",
        err
      );

      setError(
        getApiErrorMessage(
          err,
          "Failed to start interview."
        )
      );
    } finally {
      setStartingInterview(false);
    }
  };

  /*
   * Return to the resume upload page.
   */
  const handleBack = () => {
    navigate("/");
  };

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      {/* Page header */}
      <div>
        <h1 className="text-3xl font-bold">
          Configure Your Interview
        </h1>

        <p className="mt-2 text-gray-600">
          Customize your interview before starting.
        </p>
      </div>

      {/* API / validation error */}
      {error && (
        <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        className="mt-8 rounded-xl border bg-white p-6 shadow-sm"
      >
        {/* Difficulty */}
        <div>
          <label
            htmlFor="difficulty"
            className="block text-sm font-medium text-gray-700"
          >
            Difficulty
          </label>

          <select
            id="difficulty"
            value={difficulty}
            onChange={(event) =>
              setDifficulty(event.target.value)
            }
            disabled={startingInterview}
            className="mt-2 w-full rounded-lg border border-gray-300 px-3 py-2.5 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-200"
          >
            <option value="EASY">
              Easy
            </option>

            <option value="MEDIUM">
              Medium
            </option>

            <option value="HARD">
              Hard
            </option>
          </select>
        </div>

        {/* Question count */}
        <div className="mt-6">
          <label
            htmlFor="questionCount"
            className="block text-sm font-medium text-gray-700"
          >
            Number of Questions
          </label>

          <input
            id="questionCount"
            type="number"
            min="5"
            max="30"
            value={questionCount}
            onChange={(event) =>
              setQuestionCount(
                Number(event.target.value)
              )
            }
            disabled={startingInterview}
            className="mt-2 w-full rounded-lg border border-gray-300 px-3 py-2.5 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-200"
          />

          <p className="mt-1 text-xs text-gray-500">
            Choose between 5 and 30 questions.
          </p>
        </div>

        {/* Personalization */}
        <div className="mt-6">
          <h2 className="text-sm font-medium text-gray-700">
            Personalize Interview
          </h2>

          <p className="mt-1 text-xs text-gray-500">
            Select the candidate information that
            should be used for personalization.
          </p>

          <div className="mt-4 space-y-3">
            {/* Skills */}
            <label className="flex cursor-pointer items-center gap-3">
              <input
                type="checkbox"
                checked={useSkills}
                onChange={(event) =>
                  setUseSkills(
                    event.target.checked
                  )
                }
                disabled={startingInterview}
                className="h-4 w-4 rounded border-gray-300"
              />

              <span className="text-sm text-gray-700">
                Skills
              </span>
            </label>

            {/* Projects */}
            <label className="flex cursor-pointer items-center gap-3">
              <input
                type="checkbox"
                checked={useProjects}
                onChange={(event) =>
                  setUseProjects(
                    event.target.checked
                  )
                }
                disabled={startingInterview}
                className="h-4 w-4 rounded border-gray-300"
              />

              <span className="text-sm text-gray-700">
                Projects
              </span>
            </label>

            {/* Experience */}
            <label className="flex cursor-pointer items-center gap-3">
              <input
                type="checkbox"
                checked={useExperience}
                onChange={(event) =>
                  setUseExperience(
                    event.target.checked
                  )
                }
                disabled={startingInterview}
                className="h-4 w-4 rounded border-gray-300"
              />

              <span className="text-sm text-gray-700">
                Experience
              </span>
            </label>

            {/* Resume */}
            <label className="flex cursor-pointer items-center gap-3">
              <input
                type="checkbox"
                checked={useResume}
                onChange={(event) =>
                  setUseResume(
                    event.target.checked
                  )
                }
                disabled={startingInterview}
                className="h-4 w-4 rounded border-gray-300"
              />

              <span className="text-sm text-gray-700">
                Resume
              </span>
            </label>
          </div>
        </div>

        {/* Action buttons */}
        <div className="mt-8 flex gap-3">
          {/* Back button */}
          <button
            type="button"
            onClick={handleBack}
            disabled={startingInterview}
            className="rounded-lg border border-gray-300 px-5 py-2.5 font-medium text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Back
          </button>

          {/* Start interview */}
          <button
            type="submit"
            disabled={
              startingInterview ||
              questionCount < 5 ||
              questionCount > 30 ||
              (!useSkills &&
                !useProjects &&
                !useExperience &&
                !useResume)
            }
            className="flex-1 rounded-lg bg-green-600 px-5 py-2.5 font-medium text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {startingInterview
              ? "Starting Interview..."
              : "Start Interview"}
          </button>
        </div>
      </form>
    </div>
  );
}

export default InterviewConfiguration;