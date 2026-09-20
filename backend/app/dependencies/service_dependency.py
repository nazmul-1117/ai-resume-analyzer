from app.services.chat_service import AIChatService
from app.services.resume_service import ResumeService

def get_ai_service() -> AIChatService:
    return AIChatService()

def get_resume_service() -> ResumeService:
    return ResumeService()