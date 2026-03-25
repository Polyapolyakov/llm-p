from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Конфигурация приложения, загружаемая из .env"""

    # Чтение переменных окружения из файла .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App настройки
    APP_NAME: str = "llm-p"
    ENV: str = "local"

    # JWT настройки
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database (путь к SQLite)
    SQLITE_PATH: str = "./app.db"

    # OpenRouter настройки
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "stepfun/step-3.5-flash:free"
    OPENROUTER_SITE_URL: str = "https://example.com"
    OPENROUTER_APP_NAME: str = "llm-fastapi-openrouter"

# Создаем единственный экземпляр для импорта в других частях проекта
settings = Settings()
