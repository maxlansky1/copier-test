"""
Пример ORM-модели пользователя.

Содержит:
- User — модель пользователя
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ...sqlite.core import Base


class User(Base):
    """
    ORM-модель пользователя.

    Атрибуты:
        id (int): Уникальный идентификатор
        username (str): Имя пользователя
        email (str): Email пользователя
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"