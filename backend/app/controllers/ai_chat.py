from typing import Annotated
from fastapi import Depends

from app.services.ai_chat import AIChatService
from app.schemas.chat_schema import ChatRequest


def get_ai_service() -> AIChatService:
    return AIChatService()

async def ai_chat(
        request: ChatRequest,
        service: Annotated[AIChatService, Depends(get_ai_service)]
) -> dict[str, str]:
    
    return {
        "message": service.chat(
            user_message=request.message.strip(),
        )
    }