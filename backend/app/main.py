from fastapi import FastAPI
from app.routers.resume import router as resume_router
from app.routers.interview import router as interview_router
from app.routers.answer import router as answer_router
from app.routers.result import router as result_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Interview Platform",
    description="Platform for a quick interview preparation.",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def app_info():
    return "AI Interview Platform"


# Register the resume router
app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(answer_router)
app.include_router(result_router)
