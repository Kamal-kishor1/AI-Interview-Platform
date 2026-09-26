import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { startInterview } from "../services/api/interviewApi";
import { uploadResume } from "../services/api/resumeApi";


function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [candidate, setCandidate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();
  const [startingInterview, setStartingInterview] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setError("");
    setCandidate(null);

    if (!selectedFile) {
      setFile(null);
      return;
    }

    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      setError("Please upload a PDF or DOCX file.");
      setFile(null);
      return;
    }

    if (selectedFile.size > 5 * 1024 * 1024) {
      setError("File size must be less than 5 MB.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
  if (!name.trim()) {
    setError("Please enter your name.");
    return;
  }

  if (!email.trim()) {
    setError("Please enter your email.");
    return;
  }

  if (!file) {
    setError("Please select a resume first.");
    return;
  }

  try {
    setLoading(true);
    setError("");

    const data = await uploadResume(file, name, email);

    setCandidate(data);
  } catch (err) {
    console.error("Resume upload error:", err);

    const detail = err.response?.data?.detail;

    if (Array.isArray(detail)) {
      setError(
        detail
          .map((item) => item.msg)
          .filter(Boolean)
          .join(", ")
      );
    } else if (typeof detail === "string") {
      setError(detail);
    } else {
      setError("Failed to upload resume.");
    }
  } finally {
    setLoading(false);
  }
  };

  const handleStartInterview = async () => {
  if (!candidate?.id) {
    setError("Candidate information is missing.");
    return;
  }

  try {
    setStartingInterview(true);
    setError("");

    console.log("Starting interview for candidate:", candidate.id);

    const data = await startInterview(candidate.id);

    console.log("Interview started:", data);

    navigate(`/interview/${data.interview_id}`, {
      state: data,
    });
  } catch (err) {
    console.error("Start interview error:", err);

    const detail = err.response?.data?.detail;

    if (Array.isArray(detail)) {
      setError(
        detail
          .map((item) => item.msg)
          .filter(Boolean)
          .join(", ")
      );
    } else if (typeof detail === "string") {
      setError(detail);
    } else {
      setError("Failed to start interview.");
    }
  } finally {
    setStartingInterview(false);
  }
};

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-3xl font-bold">
        Upload Your Resume
      </h1>

      <p className="mt-2 text-gray-600">
        Upload your PDF or DOCX resume to begin your interview.
      </p>

      <div className="space-y-4">
        <div>
          <label
            htmlFor="name"
            className="block text-sm font-medium text-gray-700"
          >
            Full Name
          </label>

          <input
            id="name"
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Enter your full name"
            className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-2.5 outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-700"
          >
            Email
          </label>

          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="Enter your email"
            className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-2.5 outline-none focus:border-blue-500"
          />
        </div>
      </div>

      <div className="mt-8 rounded-xl border bg-white p-6 shadow-sm">
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          className="block w-full"
        />

        {file && (
          <p className="mt-3 text-sm text-gray-600">
            Selected: {file.name}
          </p>
        )}

        {error && (
          <p className="mt-4 text-sm text-red-600">
            {error}
          </p>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || !name.trim() || !email.trim() || loading}
          className="mt-6 rounded-lg bg-blue-600 px-5 py-2.5 font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Uploading..." : "Upload Resume"}
        </button>
      </div>

      {candidate && (
        <div className="mt-8 rounded-xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold">
            Resume Processed
          </h2>

          <div className="mt-4 space-y-2">
            <p>
              <strong>Name:</strong> {candidate.name}
            </p>

            <p>
              <strong>Email:</strong> {candidate.email}
            </p>

            <p>
              <strong>Resume:</strong> {candidate.resume_filename}
            </p>

            <p>
              <strong>Interview Type:</strong>{" "}
              {candidate.interview_type}
            </p>

            <p>
              <strong>Candidate ID:</strong> {candidate.id}
            </p>
          </div>

          <button
          onClick={handleStartInterview}
          disabled={startingInterview}
          className="mt-6 rounded-lg bg-green-600 px-5 py-2.5 font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
        >
          {startingInterview
            ? "Starting Interview..."
            : "Start Interview"}
        </button>
        </div>
      )}
    </div>
  );
}

export default ResumeUpload;