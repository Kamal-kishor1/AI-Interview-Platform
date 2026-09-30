import { useState } from "react";

/*
 * InterviewConfiguration
 *
 * Purpose:
 * - Collect interview configuration from the user.
 * - Validate the configuration on the frontend.
 * - Send the configuration to the parent component.
 *
 * The backend remains the final authority for validation.
 */
function InterviewConfiguration({
  candidate,
  startingInterview,
  error,
  onStartInterview,
  onBack,
}) {
    
  // Default interview configuration.
  const [difficulty, setDifficulty] = useState("MEDIUM");
  const [questionCount, setQuestionCount] = useState(10);

  // All personalization sources are enabled by default.
  const [useSkills, setUseSkills] = useState(true);
  const [useProjects, setUseProjects] = useState(true);
  const [useExperience, setUseExperience] = useState(true);
  const [useResume, setUseResume] = useState(true);


  const handleSubmit = (event) => {
    event.preventDefault();

    /*
     * Frontend validation.
     *
     * Backend validation still handles the authoritative
     * validation rules.
     */
    if (questionCount < 5 || questionCount > 30) {
      return;
    }

    /*
     * At least one personalization source must be selected.
     */
    if (
      !useSkills &&
      !useProjects &&
      !useExperience &&
      !useResume
    ) {
      return;
    }

    /*
     * Send the complete configuration to ResumeUpload.
     */
    onStartInterview({
      candidate_id: candidate.id,
      difficulty,
      question_count: questionCount,
      use_skills: useSkills,
      use_projects: useProjects,
      use_experience: useExperience,
      use_resume: useResume,
    });
  };

  return (
    <div className="mt-8 rounded-xl border bg-white p-6 shadow-sm">
      {/* Configuration heading */}
      <div>
        <h2 className="text-xl font-semibold">
          Configure Your Interview
        </h2>

        <p className="mt-1 text-sm text-gray-600">
          Customize the interview before you start.
        </p>
      </div>

      {/* Candidate / detected interview information */}
      <div className="mt-5 rounded-lg bg-gray-50 p-4">
        <p className="text-sm">
          <strong>Candidate:</strong> {candidate.name}
        </p>

        <p className="mt-1 text-sm">
          <strong>Interview Type:</strong>{" "}
          {candidate.interview_type}
        </p>
      </div>

      {/* Display backend/API error */}
      {error && (
        <div className="mt-5 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="mt-6 space-y-6">
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
            <option value="EASY">Easy</option>
            <option value="MEDIUM">Medium</option>
            <option value="HARD">Hard</option>
          </select>
        </div>

        {/* Question count */}
        <div>
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
              setQuestionCount(Number(event.target.value))
            }
            disabled={startingInterview}
            className="mt-2 w-full rounded-lg border border-gray-300 px-3 py-2.5 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-200"
          />

          <p className="mt-1 text-xs text-gray-500">
            Choose between 5 and 30 questions.
          </p>
        </div>

        {/* Personalization */}
        <div>
          <h3 className="text-sm font-medium text-gray-700">
            Personalize Interview
          </h3>

          <p className="mt-1 text-xs text-gray-500">
            Select which candidate information should be
            considered when generating questions.
          </p>

          <div className="mt-4 space-y-3">
            {/* Skills */}
            <label className="flex cursor-pointer items-center gap-3">
              <input
                type="checkbox"
                checked={useSkills}
                onChange={(event) =>
                  setUseSkills(event.target.checked)
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
                  setUseProjects(event.target.checked)
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
                  setUseExperience(event.target.checked)
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
                  setUseResume(event.target.checked)
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
        <div className="flex gap-3 pt-2">
          <button
            type="button"
            onClick={onBack}
            disabled={startingInterview}
            className="rounded-lg border border-gray-300 px-5 py-2.5 font-medium text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Back
          </button>

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