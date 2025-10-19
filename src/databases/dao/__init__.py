"""
Модуль для работы с DAO (Data Access Objects)
"""

from .base import BaseDAO
from .user_dao import UserDAO

__all__ = [
    "BaseDAO",
    "UserDAO",
]
