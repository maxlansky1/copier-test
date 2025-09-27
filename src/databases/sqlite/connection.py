"""
Модуль для получения сессии БД.

Содержит:
- get_db_session — генератор сессии (для использования в FastAPI Depends)
"""

from typing import AsyncGenerator
from .core import async_session


async def get_db_session() -> AsyncGenerator:
    """
    Асинхронный генератор сессии БД.

    Используется для внедрения зависимости в FastAPI.
    Автоматически закрывает сессию после использования.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()