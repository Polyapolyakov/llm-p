class AppError(Exception):
    """Базовое исключение приложения."""
    pass

class ConflictError(AppError):
    """Ресурс уже существует (например, email)."""
    pass

class UnauthorizedError(AppError):
    """Неверные учетные данные."""
    pass

class ForbiddenError(AppError):
    """Недостаточно прав."""
    pass

class NotFoundError(AppError):
    """Объект не найден."""
    pass

class ExternalServiceError(AppError):
    """Ошибка при обращении к внешнему сервису (OpenRouter)."""
    pass
