from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Пароль не короче 6 символов")
    
    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """
        Проверяет, что email соответствует формату student_surname@email.com
        """
        # Паттерн: любое имя (student_surname) @ email.com
        # student_surname может содержать буквы, цифры, подчеркивания
        pattern = r'^[a-zA-Z0-9_]+@email\.com$'
        
        if not re.match(pattern, v):
            raise ValueError(
                'Email должен быть в формате student_surname@email.com. '
                'Пример: ivan_ivanov@email.com'
            )
        
        # Дополнительная проверка: имя не должно быть пустым
        local_part = v.split('@')[0]
        if not local_part:
            raise ValueError('Имя пользователя в email не может быть пустым')
        
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
