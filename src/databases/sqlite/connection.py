"""
Модуль для получения асинхронной сессии базы данных.

Содержит:
- get_db_session — асинхронный генератор сессии для использования с FastAPI Depends
"""

from typing import AsyncGenerator

from .core import async_session


async def get_db_session() -> AsyncGenerator:
    """
    Асинхронный генератор сессии базы данных.

    Используется для внедрения зависимости в FastAPI-маршруты.
    Обеспечивает автоматическое открытие и закрытие сессии при каждом запросе.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy для выполнения запросов к БД.

    Example:
        from fastapi import Depends
        from sqlalchemy.ext.asyncio import AsyncSession

        async def get_user_list(db: AsyncSession = Depends(get_db_session)):
            # Работа с сессией
            pass
    """
    async with async_session() as session:
        try:
            # Возвращаем сессию для использования в маршруте
            yield session
        finally:
            # Гарантируем закрытие сессии после завершения
            await session.close()
