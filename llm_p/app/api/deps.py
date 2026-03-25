from typing import Annotated, AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency для получения сессии БД
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Предоставляет сессию базы данных."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Dependency для репозиториев
async def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> UserRepository:
    return UserRepository(session)

async def get_chat_repo(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> ChatMessageRepository:
    return ChatMessageRepository(session)

# Dependency для сервисов
def get_openrouter_client() -> OpenRouterClient:
    return OpenRouterClient()

# Dependency для usecases
async def get_auth_usecase(
    user_repo: Annotated[UserRepository, Depends(get_user_repo)]
) -> AuthUseCase:
    return AuthUseCase(user_repo)

async def get_chat_usecase(
    chat_repo: Annotated[ChatMessageRepository, Depends(get_chat_repo)],
    openrouter_client: Annotated[OpenRouterClient, Depends(get_openrouter_client)]
) -> ChatUseCase:
    return ChatUseCase(chat_repo, openrouter_client)

# Dependency для получения текущего пользователя
async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> int:
    """
    Извлекает user_id из JWT токена.
    """
    try:
        payload = security.decode_token(token)
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен",
            )
        return int(user_id_str)
    except (ValueError, JWTError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
        ) from e
