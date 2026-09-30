from app.parsers.docx_parser import DOCXResumeParser
from app.parsers.pdf_parser import PDFResumeParser

from app.services.chat_service import AIChatService
from app.services.resume_service import ResumeService
from app.services.resume_structurer import ResumeStructurer

from app.utils.text_cleaner import TextCleaner

def get_ai_service() -> AIChatService:
    return AIChatService()

def get_resume_service() -> ResumeService:
    return ResumeService(
        pdf_parser=PDFResumeParser(),
        docx_parser=DOCXResumeParser(),
        text_cleaner=TextCleaner(),
        resume_structurer = ResumeStructurer(),
    )