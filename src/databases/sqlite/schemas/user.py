"""
Схемы Pydantic для пользователей.

В этом модуле определены схемы для сериализации,
валидации данных при создании и обновлении пользователей.

- `UserPydantic` — схема для вывода данных пользователя (например, в API-ответе).
- `UserCreateSchema` — схема для валидации данных при создании нового пользователя.
- `UserUpdateSchema` — схема для валидации данных при обновлении существующего пользователя.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserPydantic(BaseModel):
    """Схема для сериализации пользователя.

    Используется для формирования ответа API или возврата данных
    пользователю. Поддерживает создание из ORM-модели через `.from_orm()`.
    """

    id: int
    username: str
    email: str

    model_config = ConfigDict(
        from_attributes=True,  # Позволяет создавать схему из ORM-объектов
    )


class UserCreateSchema(BaseModel):
    """Схема для валидации данных при создании нового пользователя.

    Все поля обязательны для заполнения при создании пользователя.
    """

    username: str
    email: EmailStr  # Валидирует корректность email
    password: str  # Пароль обязательно для создания


class UserUpdateSchema(BaseModel):
    """Схема для валидации данных при обновлении существующего пользователя.

    Все поля являются опциональными, кроме пароля, который обновляется
    отдельным эндпоинтом при необходимости.
    """

    username: Optional[str] = None
    email: Optional[EmailStr] = None
