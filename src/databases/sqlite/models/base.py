"""
Базовый класс для всех ORM-моделей.

Содержит универсальные колонки:
- id: уникальный идентификатор записи
- created_at: дата и время создания записи
- updated_at: дата и время последнего обновления записи

Автоматически формирует имя таблицы (например, User -> users).
"""

from datetime import datetime

from sqlalchemy import Integer, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    class_mapper,
    declared_attr,
    mapped_column,
)


class Base(DeclarativeBase):
    """
    Базовый класс для всех ORM-моделей.

    Содержит универсальные колонки:
    - id: уникальный идентификатор записи
    - created_at: дата и время создания записи
    - updated_at: дата и время последнего обновления записи

    Автоматически формирует имя таблицы (например, User -> users).
    """

    __abstract__ = True  # Не создает таблицу в БД

    # Универсальные колонки для всех моделей
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Автоматически формирует имя таблицы: User -> users, Post -> posts
        return cls.__name__.lower() + "s"

    def to_dict(self) -> dict:
        """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
        columns = class_mapper(self.__class__).columns
        return {column.key: getattr(self, column.key) for column in columns}
