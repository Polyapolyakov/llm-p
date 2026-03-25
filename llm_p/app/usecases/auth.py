from app.core import security
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.repositories.users import UserRepository
from app.schemas.user import UserPublic

class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, email: str, password: str) -> UserPublic:
        # 1. Проверяем, существует ли пользователь
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise ConflictError("Пользователь с таким email уже существует")

        # 2. Хешируем пароль
        hashed_password = security.get_password_hash(password)

        # 3. Создаем пользователя
        user = await self.user_repo.create(email, hashed_password)
        return UserPublic.model_validate(user)

    async def login(self, email: str, password: str) -> str:
        # 1. Ищем пользователя
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Неверный email или пароль")

        # 2. Проверяем пароль
        if not security.verify_password(password, user.password_hash):
            raise UnauthorizedError("Неверный email или пароль")

        # 3. Создаем и возвращаем токен
        token_data = {"sub": str(user.id), "role": user.role}
        return security.create_access_token(data=token_data)

    async def get_profile(self, user_id: int) -> UserPublic:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")
        return UserPublic.model_validate(user)
