from pydantic import BaseModel, Field
from typing import Literal, Optional

class EmotionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    model: Optional[Literal["auto", "gemini", "local"]] = Field(
        default="auto",
        description="Which model to use: 'gemini', 'local', or 'auto' (Gemini first, fallback to local)"
    )

class EmotionResponse(BaseModel):
    emotion: str
    confidence: float
    source: str
