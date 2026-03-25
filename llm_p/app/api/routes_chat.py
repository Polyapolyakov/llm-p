from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.errors import ExternalServiceError
from app.schemas import chat as chat_schemas
from app.api import deps
from app.usecases.chat import ChatUseCase

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=chat_schemas.ChatResponse)
async def chat(
    request: chat_schemas.ChatRequest,
    user_id: Annotated[int, Depends(deps.get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(deps.get_chat_usecase)]
):
    """
    Отправляет запрос к LLM и возвращает ответ.
    - prompt: текст запроса пользователя
    - system: опциональная системная инструкция
    - max_history: количество последних сообщений для контекста (по умолчанию 10)
    - temperature: креативность ответа (по умолчанию 0.7)
    """
    try:
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=request.prompt,
            system_instruction=request.system,
            max_history=request.max_history,
            temperature=request.temperature,
        )
        return chat_schemas.ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )

@router.get("/history", response_model=List[chat_schemas.MessageResponse])
async def get_history(
    user_id: Annotated[int, Depends(deps.get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(deps.get_chat_usecase)],
    limit: int = 100
):
    """
    Возвращает историю сообщений текущего пользователя.
    - limit: максимальное количество сообщений (по умолчанию 100)
    """
    messages = await chat_usecase.get_history(user_id, limit)
    # Преобразуем ORM объекты в Pydantic схемы
    return [chat_schemas.MessageResponse.model_validate(msg) for msg in messages]

@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: Annotated[int, Depends(deps.get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(deps.get_chat_usecase)]
):
    """
    Очищает всю историю сообщений текущего пользователя.
    """
    await chat_usecase.clear_history(user_id)
    return None
