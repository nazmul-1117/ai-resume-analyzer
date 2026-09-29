from fastapi import APIRouter,  status

from app.controllers.resume_controller import analyze_resume
from app.schemas.resume_schema import ResumeAnalysisResponse, ResumeProfile

resume_router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

# resume_router.add_api_route(
#     path="/analyze",
#     endpoint=analyze_resume,
#     methods=["POST"],
#     status_code=status.HTTP_200_OK,
#     response_model=ResumeAnalysisResponse,
#     summary="Analyze a resume",
#     description=(
#         "Upload a PDF resume, extract its text, clean the extracted "
#         "content, and return the processed resume content."
#     ),
# )

resume_router.post(
    path="/analyze",
    status_code=status.HTTP_200_OK,
    response_model=ResumeProfile,
    
    summary="Analyze a Resume",
    description=(
        "Upload a PDF or DOCX resume, extract its text, clean the extracted content, "
        "and return the processed resume content."
    ),
)(analyze_resume)