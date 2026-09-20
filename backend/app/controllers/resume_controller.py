from typing import Annotated
from fastapi import UploadFile, status, Depends

from app.dependencies.service_dependency import get_resume_service

from app.services.resume_service import ResumeService

async def analyze_resume(
        file: UploadFile,

        service: Annotated[ResumeService, Depends(get_resume_service)],
):

    content: str = await service.analyze_resume(file=file)

    return {
        "status_code": status.HTTP_200_OK,
        "file_name": file.filename,
        "file_size": file.size,
        "file_type": file.content_type,
        "file_header": file.headers,

        "content": content,
    }