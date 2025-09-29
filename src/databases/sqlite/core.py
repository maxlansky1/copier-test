"""
Модуль для создания асинхронного движка и сессии SQLAlchemy.

Содержит:
- Base — базовый класс для ORM-моделей
- engine — асинхронный движок
- async_session — фабрика асинхронных сессий
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from configs.settings import settings

# Базовый класс для всех ORM-моделей
Base = declarative_base()

# Создаём асинхронный движок с настройками из конфига
engine = create_async_engine(
    settings.database.sqlite.database_url,
    echo=settings.database.sqlite.echo,
    pool_pre_ping=settings.database.sqlite.pool_pre_ping,
    pool_size=settings.database.sqlite.pool_size,
    max_overflow=settings.database.sqlite.max_overflow,
)

# Фабрика асинхронных сессий
async_session = async_sessionmaker(
    engine,
    expire_on_commit=settings.database.sqlite.expire_on_commit,
    autoflush=settings.database.sqlite.autoflush,
)