from fastapi import UploadFile

from app.schemas.resume_schema import ResumeProfile
from app.parsers.docx_parser import DOCXResumeParser
from app.parsers.pdf_parser import PDFResumeParser
from app.utils.text_cleaner import TextCleaner

from app.services.resume_structurer import ResumeStructurer

class ResumeService:

    ALLOWED_CONTENT_TYPES = {
        "application/pdf",
        (
            "application/"
            "vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
    }

    MAX_FILE_SIZE = 5*1024*1024 # 5 MB

    def __init__(
            self,
            pdf_parser: PDFResumeParser,
            docx_parser: DOCXResumeParser,
            text_cleaner: TextCleaner,
            resume_structurer: ResumeStructurer,
    ):
        self.pdf_parser = pdf_parser
        self.docx_parser = docx_parser
        self.text_cleaner = text_cleaner
        self.resume_structurer = resume_structurer

    async def analyze_resume(
            self,
            *,
            file: UploadFile | None = None
    ) -> ResumeProfile:

        self._validate_file(file=file)

        file_bytes = await file.read()

        self._validate_file_size(
            file_bytes=file_bytes
        )

        raw_text = await self._extract_text(
            file=file,
            file_bytes=file_bytes,
        )

        cleaned_text = self.text_cleaner.clean(
            raw_text=raw_text
        )

        if not cleaned_text:
            raise ValueError(
                "Not readable text could be extracted from the resume."
            )

        resume_profile = self.resume_structurer.structure(
            text=cleaned_text
        )

        print(cleaned_text)

        return resume_profile

    def _validate_file(
            self,
            *,
            file: UploadFile,
    ) -> None:
        
        if not file.filename:
            raise ValueError(
                "Resume file is required"
            )

        if file.content_type not in self.ALLOWED_CONTENT_TYPES:
            raise ValueError(
                "Only PDF and DOCX files are supported "
                f"But you given {file.content_type}"
            )

    def _validate_file_size(
            self,
            *,
            file_bytes: bytes
    ) -> None:

        if not file_bytes:
            raise ValueError(
                "Uploaded file is empty"
            )

        if len(file_bytes) > self.MAX_FILE_SIZE:
            raise ValueError(
                "Resume file size must not exceed 5 MB "
                f"But you given {len(file_bytes)/(1024*1024)} MB"
            )

    async def _extract_text(
            self,
            *,
            file: UploadFile,
            file_bytes: bytes
    ) -> str:

        if file.content_type == "application/pdf":
            return await self.pdf_parser.extract_text(
                file_bytes=file_bytes
            )

        if (
            file.content_type == (
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        ):
            return await self.docx_parser.extract_text(
                file_bytes=file_bytes,
            )

        raise ValueError(
            "Unsupported resume format."
        )


    def _save_file(
            self,
            *,
            file: UploadFile
    ):
        ...

