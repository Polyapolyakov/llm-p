import httpx
from typing import List, Dict

from app.core.config import settings
from app.core.errors import ExternalServiceError

class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_APP_NAME,
            "Content-Type": "application/json",
        }

    async def ask(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        Отправляет запрос в OpenRouter.
        messages: список словарей [{"role": "user/system/assistant", "content": "текст"}]
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                )
                # Выбросит исключение для 4xx/5xx (oшибка клиента/oшибка сервера)
                response.raise_for_status()
                data = response.json()
                # Извлекаем ответ
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                raise ExternalServiceError(f"Ошибка от OpenRouter: {e.response.status_code} - {e.response.text}") from e
            except Exception as e:
                raise ExternalServiceError(f"Ошибка при обращении к OpenRouter: {e}") from e
