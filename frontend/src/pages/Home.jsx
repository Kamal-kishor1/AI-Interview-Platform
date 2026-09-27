import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="mx-auto max-w-5xl px-6 py-16">
      {/* Hero */}
      <section className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
          AI Interview Platform
        </h1>

        <p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-gray-600">
          Practice technical interviews with questions based on
          your resume and receive a structured interview result.
        </p>

        <Link
          to="/resume"
          className="mt-8 inline-block rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700"
        >
          Start Your Interview
        </Link>
      </section>

      {/* How it works */}
      <section className="mt-16">
        <h2 className="text-center text-2xl font-semibold text-gray-900">
          How It Works
        </h2>

        <div className="mt-8 grid gap-6 md:grid-cols-3">
          <div className="rounded-xl border bg-white p-6 shadow-sm">
            <div className="text-2xl font-bold text-blue-600">
              01
            </div>

            <h3 className="mt-4 text-lg font-semibold">
              Upload Resume
            </h3>

            <p className="mt-2 text-gray-600">
              Upload your PDF or DOCX resume and provide your
              basic candidate information.
            </p>
          </div>

          <div className="rounded-xl border bg-white p-6 shadow-sm">
            <div className="text-2xl font-bold text-blue-600">
              02
            </div>

            <h3 className="mt-4 text-lg font-semibold">
              Take Interview
            </h3>

            <p className="mt-2 text-gray-600">
              Answer technical questions based on the interview
              type detected from your resume.
            </p>
          </div>

          <div className="rounded-xl border bg-white p-6 shadow-sm">
            <div className="text-2xl font-bold text-blue-600">
              03
            </div>

            <h3 className="mt-4 text-lg font-semibold">
              View Result
            </h3>

            <p className="mt-2 text-gray-600">
              Complete the interview and view your interview
              completion summary.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;