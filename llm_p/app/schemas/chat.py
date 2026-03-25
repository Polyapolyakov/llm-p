from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    """Запрос к LLM."""
    
    prompt: str = Field(..., description="Текст запроса пользователя")
    system: Optional[str] = Field(None, description="Системная инструкция")
    max_history: int = Field(
        10,
        ge=1,
        le=50,
        description="Количество последних сообщений для контекста"
    )
    temperature: float = Field(
        0.7,
        ge=0.0,
        le=2.0,
        description="Температура (креативность) ответа"
    )

class ChatResponse(BaseModel):
    """Ответ LLM."""
    
    answer: str = Field(..., description="Сгенерированный ответ")

class MessageResponse(BaseModel):
    """Схема одного сообщения в истории."""
    
    id: int
    user_id: int
    role: str  # 'user' или 'assistant'
    content: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
