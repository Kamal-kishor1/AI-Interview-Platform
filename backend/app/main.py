from fastapi import FastAPI
from app.routers.resume import router as resume_router
from app.routers.interview import router as interview_router
from app.routers.answer import router as answer_router
from app.routers.result import router as result_router
from app.routers.evaluation import router as evaluation_router
from app.routers.ai_evaluation import router as ai_evaluation_router
from app.routers.candidate import router as candidate_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Interview Platform API",
    description="Platform for a quick interview preparation.",
    version="1.0.0",
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
app.include_router(candidate_router)
app.include_router(interview_router)
app.include_router(answer_router)
app.include_router(result_router)
app.include_router(evaluation_router)
app.include_router(ai_evaluation_router)
