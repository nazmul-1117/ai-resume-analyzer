from fastapi import APIRouter, status

from app.controllers.ai_chat import ai_chat

chat_router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)

chat_router.post(
    path="",
    status_code=status.HTTP_200_OK,
    description="Chat with AI",
)(ai_chat)
