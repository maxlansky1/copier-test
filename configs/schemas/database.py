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


class DatabaseSettings(BaseConfig):
    """
    Общие настройки для всех баз данных.
    """

    sqlite: SQLiteSettings = SQLiteSettings()
