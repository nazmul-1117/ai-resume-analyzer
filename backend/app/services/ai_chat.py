from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

from app.core.config import settings

class AIChatService:

    def __init__(
            self,
    ):
        self.llm = ChatOpenAI(
            api_key= settings.API_KEY,
            base_url= settings.BASE_URL,
            model=settings.AI_MODEL,
        )

    def chat(
            self,
            *,
            user_message: str,
            context: list[str] | None = None
    ) -> str | list:

        messages = [
            SystemMessage(
                content=(
                    "You are an AI Resume Assistant. "
                    "Help users understand and improve their resumes "
                    "and provide professional career-related guidance."
                ),
            ),
        ]

        if context:
            for message in context:
                messages.append(HumanMessage(content=message))

        messages.append(HumanMessage(content=user_message))

        result = self.llm.invoke(messages)

        return result.content