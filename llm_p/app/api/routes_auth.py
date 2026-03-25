from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.schemas import auth as auth_schemas, user as user_schemas
from app.api import deps
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=user_schemas.UserPublic)
async def register(
    user_data: auth_schemas.RegisterRequest,
    auth_usecase: Annotated[AuthUseCase, Depends(deps.get_auth_usecase)]
):
    """
    Регистрация нового пользователя.
    Требования к email:
    - Должен быть в формате student_surname@email.com
    - Пример: ivan_ivanov@email.com
    Требования к паролю:
    - Минимальная длина 6 символов
    """
    try:
        user = await auth_usecase.register(user_data.email, user_data.password)
        return user
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/login", response_model=auth_schemas.TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_usecase: Annotated[AuthUseCase, Depends(deps.get_auth_usecase)]
):
    """OAuth2 совместимый логин. Используйте 'username' поле для email."""
    try:
        token = await auth_usecase.login(form_data.username, form_data.password)
        return auth_schemas.TokenResponse(access_token=token)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.get("/me", response_model=user_schemas.UserPublic)
async def get_my_profile(
    user_id: Annotated[int, Depends(deps.get_current_user_id)],
    auth_usecase: Annotated[AuthUseCase, Depends(deps.get_auth_usecase)]
):
    try:
        return await auth_usecase.get_profile(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
