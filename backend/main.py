from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
 
API_VERSION: str = "v1"
API_PREFIX: str = f"api/{API_VERSION}"

app = FastAPI(
    title="AI Resume Analyzer",
    description="An AI-powered resume analyzer that uses FastAPI, PDF processing, and LLM technology to analyze resumes and provide structured feedback, skills analysis, resume scoring, and personalized improvement suggestions.",
    version= API_VERSION,
)



@app.get("/")
def root() -> dict:

    return {
        "Name": "AI Resume Analyzer",
        "Description": "An AI-powered resume analyzer that uses FastAPI, PDF processing, and LLM technology to analyze resumes and provide structured feedback, skills analysis, resume scoring, and personalized improvement suggestions.",
        "API_VERSION": API_VERSION
    }