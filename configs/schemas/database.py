# configs/schemas/databases.py

"""
Схемы конфигурации для баз данных.
"""

from pydantic import Field

from .base import BaseConfig


class SQLiteSettings(BaseConfig):
    """
    Настройки SQLite базы данных.
    """

    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/db.sqlite3",
        description="URL подключения к SQLite базе данных",
    )
    echo: bool = Field(default=False, description="Включить логирование SQL-запросов")
    pool_pre_ping: bool = Field(
        default=True, description="Проверять соединение перед использованием"
    )
    expire_on_commit: bool = Field(
        default=False, description="Не устаревают объекты после commit"
    )
    autoflush: bool = Field(default=False, description="Отключить автоматический flush")
    pool_size: int = Field(default=5, description="Размер пула соединений")
    max_overflow: int = Field(
        default=10, description="Максимальное количество дополнительных соединений"
    )


class RedisSettings(BaseConfig):
    """
    Настройки Redis.
    """

    redis_url: str = Field(
        default="redis://default:password@redis:6379/0",
        description="URL подключения к Redis. В Docker используй имя сервиса: redis://user:password@redis:6379/0"
    )
    redis_db: int = Field(
        default=0,
        description="Номер базы Redis (0-15)"
    )
    redis_ttl: int = Field(
        default=3600,
        description="Время жизни ключей по умолчанию в секундах"
    )
    decode_responses: bool = Field(
        default=True,
        description="Декодировать ответы Redis в строки (удобно для работы с текстовыми данными)"
    )


class DatabaseSettings(BaseConfig):
    """
    Общие настройки для всех баз данных.
    """

    sqlite: SQLiteSettings = SQLiteSettings()
    redis: RedisSettings = RedisSettings()