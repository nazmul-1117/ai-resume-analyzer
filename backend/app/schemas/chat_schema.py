from pydantic import BaseModel, ConfigDict

class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str