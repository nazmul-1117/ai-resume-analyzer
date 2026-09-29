from typing import Annotated

from fastapi import UploadFile, File, status, Depends, HTTPException

from app.dependencies.service_dependency import get_resume_service
from app.schemas.resume_schema import ResumeAnalysisResponse, ResumeProfile
from app.services.resume_service import ResumeService

async def analyze_resume(
        file: Annotated[
            UploadFile,
            File(
                ...,
                description="Resume file in PDF or DOCX fromat",
            )
        ],

        service: Annotated[
            ResumeService,
            Depends(get_resume_service),
        ],
) -> ResumeProfile:

    try:
        content: ResumeProfile = await service.analyze_resume(file=file)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        ) from exc

    return content

    # return ResumeAnalysisResponse(
    #     success=True,
    #     data = {
    #             "file_name": file.filename,
    #             "file_size": file.size,
    #             "file_type": file.content_type,
    #             "content": content,
    #         },
    # )