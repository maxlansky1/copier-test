"""
Объект доступа к данным (DAO) для работы с записями пользователей в базе данных.

В этом модуле определён класс `UserDAO`, который предоставляет асинхронные
методы для доступа и управления сущностями `User` в SQLite.
Класс наследует функционал общего `BaseDAO` и может быть расширен
специфичными методами для пользователей.

Пример использования:
    async with async_session() as session:
        users = await UserDAO.get_all_users(session)
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.databases.dao.base import BaseDAO
from src.databases.sqlite.models import User


class UserDAO(BaseDAO):
    """Объект доступа к данным для модели `User`.

    Класс предоставляет методы для работы с пользователями в базе данных.
    Наследует общий функционал `BaseDAO` и может быть дополнен
    специфичными запросами и логикой для пользователей.
    """

    model = User

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        """Получить всех пользователей из базы данных.

        Args:
            session (AsyncSession): Активная асинхронная сессия SQLAlchemy.

        Returns:
            list[User]: Список всех пользователей, сохранённых в базе данных.
        """
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()
