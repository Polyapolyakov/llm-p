from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.models import ChatMessage

class ChatMessageRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_last_messages(self, user_id: int, limit: int = 10) -> List[ChatMessage]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        # Возвращаем в хронологическом порядке (сначала старые)
        return list(reversed(result.scalars().all()))

    async def clear_history(self, user_id: int) -> None:
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()
