from typing import Annotated
from fastapi import Depends

from app.dependencies.service_dependency import get_ai_service
from app.services.chat_service import AIChatService
from app.schemas.chat_schema import ChatRequest


async def ai_chat(
        request: ChatRequest,
        service: Annotated[AIChatService, Depends(get_ai_service)]
) -> dict[str, str]:
    
    return {
        "message": service.chat(
            user_message=request.message.strip(),
        )
    }