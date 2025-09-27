"""
Модуль для создания асинхронного движка и сессии SQLAlchemy.

Содержит:
- Base — базовый класс для ORM-моделей
- engine — асинхронный движок
- async_session — фабрика асинхронных сессий
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Базовый класс для всех ORM-моделей
Base = declarative_base()

# Получаем URL подключения к БД из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./db.sqlite3")

# Создаём асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Включить True для логирования SQL-запросов
    pool_pre_ping=True,  # Проверяет соединение перед использованием
)

# Фабрика асинхронных сессий
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,  # Не устаревают объекты после commit
    autoflush=False,         # Отключаем автоматический flush
)