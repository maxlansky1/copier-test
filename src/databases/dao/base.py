"""
Базовый класс для DAO (Data Access Object).

Содержит общие методы для добавления записей в БД.
"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    """
    Базовый класс для всех DAO.

    Атрибуты:
        model: ORM-модель, с которой работает DAO.
    """

    model = None

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        """
        Добавляет одну запись в БД.

        Args:
            session: Асинхронная сессия SQLAlchemy.
            **values: Поля для создания новой записи.

        Returns:
            Новый экземпляр модели.
        """
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: list[dict]):
        """
        Добавляет несколько записей в БД.

        Args:
            session: Асинхронная сессия SQLAlchemy.
            instances: Список словарей с полями для создания записей.

        Returns:
            Список новых экземпляров модели.
        """
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        """
        Возвращает одну запись по её ID или None, если запись не найдена.
        Использует session.get() для эффективного получения по первичному ключу.
        """
        return await session.get(cls.model, data_id)

    @classmethod
    async def delete_one_by_id(cls, session: AsyncSession, data_id: int):
        """
        Удаляет одну запись по ID.
        """
        try:
            data = await session.get(cls.model, data_id)
            if data:
                await session.delete(data)
                await session.flush()
            return data
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
