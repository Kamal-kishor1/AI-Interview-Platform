function ResumeForm({
  name,
  email,
  file,
  loading,
  error,
  onNameChange,
  onEmailChange,
  onFileChange,
  onSubmit,
}) {
  return (
    <div className="space-y-4">
      {/* Name */}
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
          onChange={(event) => onNameChange(event.target.value)}
          placeholder="Enter your full name"
          disabled={loading}
          className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-2.5 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
        />
      </div>

      {/* Email */}
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
          onChange={(event) => onEmailChange(event.target.value)}
          placeholder="Enter your email"
          disabled={loading}
          className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-2.5 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
        />
      </div>

      {/* Resume upload */}
      <div className="mt-8 rounded-xl border bg-white p-6 shadow-sm">
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={onFileChange}
          disabled={loading}
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
          type="button"
          onClick={onSubmit}
          disabled={
            !file ||
            !name.trim() ||
            !email.trim() ||
            loading
          }
          className="mt-6 rounded-lg bg-blue-600 px-5 py-2.5 font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Uploading..." : "Upload Resume"}
        </button>
      </div>
    </div>
  );
}

export default ResumeForm;