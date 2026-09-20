from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers.chat_router import chat_router
from app.routers.resume_router import resume_router
 
API_VERSION: str = "v1"
API_PREFIX: str = f"/api/{API_VERSION}"

app = FastAPI(
    title="AI Resume Analyzer",
    description="An AI-powered resume analyzer that uses FastAPI, PDF processing, and LLM technology to analyze resumes and provide structured feedback, skills analysis, resume scoring, and personalized improvement suggestions.",
    version= API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=chat_router,
    prefix=API_PREFIX
)

app.include_router(
    router=resume_router,
    prefix=API_PREFIX
)



@app.get("/")
def root() -> dict:

    return {
        "Name": "AI Resume Analyzer",
        "Description": "An AI-powered resume analyzer that uses FastAPI, PDF processing, and LLM technology to analyze resumes and provide structured feedback, skills analysis, resume scoring, and personalized improvement suggestions.",
        "API_VERSION": API_VERSION
    }