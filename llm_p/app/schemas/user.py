from pydantic import BaseModel, ConfigDict, EmailStr

class UserPublic(BaseModel):
    """Публичная схема пользователя (без пароля)."""

    id: int
    email: EmailStr
    role: str

    # Конфигурация для работы FastAPI  с ORM-объектами SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
