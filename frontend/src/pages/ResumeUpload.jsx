import { useState } from "react";
import { useNavigate } from "react-router-dom";

import ResumeForm from "../components/resume/ResumeForm";
import ResumeProcessedCard from "../components/resume/ResumeProcessedCard";

import { startInterview } from "../services/api/interviewApi";
import { uploadResume } from "../services/api/resumeApi";

import { getApiErrorMessage } from "../utils/errorHandler";

function ResumeUpload() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const [candidate, setCandidate] = useState(null);

  const [loading, setLoading] = useState(false);
  const [startingInterview, setStartingInterview] =
    useState(false);

  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

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

    const maxFileSize = 5 * 1024 * 1024;

    if (selectedFile.size > maxFileSize) {
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

      const candidateData = await uploadResume(
        file,
        name,
        email
      );

      console.log(
        "Resume uploaded:",
        candidateData
      );

      setCandidate(candidateData);
    } catch (err) {
      console.error(
        "Resume upload error:",
        err
      );

      setError(
        getApiErrorMessage(
          err,
          "Failed to upload resume."
        )
      );
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

      console.log(
        "Starting interview for candidate:",
        candidate.id
      );

      const interviewData = await startInterview(
        candidate.id
      );

      console.log(
        "Interview started:",
        interviewData
      );

      /*
       * IMPORTANT:
       * Use interviewData here.
       *
       * The previous code used:
       *
       * navigate(`/interview/${data.interview_id}`)
       *
       * but `data` did not exist.
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

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      {/* Page header */}
      <div>
        <h1 className="text-3xl font-bold">
          Upload Your Resume
        </h1>

        <p className="mt-2 text-gray-600">
          Upload your PDF or DOCX resume to begin
          your interview.
        </p>
      </div>

      {/* Resume form */}
      <div className="mt-8">
        <ResumeForm
          name={name}
          email={email}
          file={file}
          loading={loading}
          error={error}
          onNameChange={(value) => {
            setName(value);
            setError("");
          }}
          onEmailChange={(value) => {
            setEmail(value);
            setError("");
          }}
          onFileChange={handleFileChange}
          onSubmit={handleUpload}
        />
      </div>

      {/* Processed candidate */}
      <ResumeProcessedCard
        candidate={candidate}
        startingInterview={startingInterview}
        onStartInterview={handleStartInterview}
      />
    </div>
  );
}

export default ResumeUpload;