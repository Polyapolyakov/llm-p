from typing import List, Dict
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.core.errors import ExternalServiceError
# Для type hinting (импорт для аннотаций типов)
from app.db.models import ChatMessage  

class ChatUseCase:
    def __init__(self, chat_repo: ChatMessageRepository, openrouter_client: OpenRouterClient):
        self.chat_repo = chat_repo
        self.openrouter_client = openrouter_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system_instruction: str | None,
        max_history: int,
        temperature: float,
    ) -> str:
        """Отправляет запрос к LLM и сохраняет диалог."""
        # 1. Собираем сообщения для контекста
        messages: List[Dict[str, str]] = []

        # Системная инструкция (если есть)
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})

        # История сообщений пользователя
        history = await self.chat_repo.get_last_messages(user_id, max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # Текущий запрос пользователя
        messages.append({"role": "user", "content": prompt})

        # 2. Сохраняем запрос пользователя в БД
        await self.chat_repo.add_message(user_id, "user", prompt)

        # 3. Отправляем запрос в OpenRouter
        try:
            answer = await self.openrouter_client.ask(messages, temperature)
        except ExternalServiceError as e:
            raise e

        # 4. Сохраняем ответ ассистента
        await self.chat_repo.add_message(user_id, "assistant", answer)

        return answer

    async def get_history(self, user_id: int, limit: int = 100) -> List[ChatMessage]:
        """
        Получает историю сообщений пользователя.
        Args:
            user_id: ID пользователя
            limit: Максимальное количество сообщений   
        Returns:
            List[ChatMessage]: Список сообщений в хронологическом порядке
        """
        return await self.chat_repo.get_last_messages(user_id, limit)

    async def clear_history(self, user_id: int) -> None:
        """
        Очищает всю историю сообщений пользователя.
        Args:
            user_id: ID пользователя
        """
        await self.chat_repo.clear_history(user_id)
