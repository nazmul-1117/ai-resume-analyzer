from fastapi import APIRouter,  status

from app.controllers.resume_controller import analyze_resume

resume_router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

resume_router.post(
    path="/analyze",
    status_code=status.HTTP_200_OK,
    description="Upload resume to analyze"
)(analyze_resume)