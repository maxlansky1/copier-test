"""
Схемы конфигурации для баз данных.
"""

from typing import Optional
from pydantic import Field
from .base import BaseConfig


class SQLiteSettings(BaseConfig):
    """
    Настройки SQLite базы данных.
    """
    database_url: str = Field(
        default="sqlite+aiosqlite:///./db.sqlite3",
        description="URL подключения к SQLite базе данных"
    )
    echo: bool = Field(
        default=False,
        description="Включить логирование SQL-запросов"
    )
    pool_pre_ping: bool = Field(
        default=True,
        description="Проверять соединение перед использованием"
    )
    expire_on_commit: bool = Field(
        default=False,
        description="Не устаревают объекты после commit"
    )
    autoflush: bool = Field(
        default=False,
        description="Отключить автоматический flush"
    )
    pool_size: int = Field(
        default=5,
        description="Размер пула соединений"
    )
    max_overflow: int = Field(
        default=10,
        description="Максимальное количество дополнительных соединений"
    )


class RedisSettings(BaseConfig):
    """
    Настройки Redis базы данных.
    """
    host: str = Field(
        default="localhost",
        description="Хост Redis сервера"
    )
    port: int = Field(
        default=6379,
        description="Порт Redis сервера"
    )
    db: int = Field(
        default=0,
        description="Номер базы данных Redis"
    )
    password: Optional[str] = Field(
        default=None,
        description="Пароль для аутентификации Redis"
    )
    ssl: bool = Field(
        default=False,
        description="Использовать SSL соединение"
    )
    decode_responses: bool = Field(
        default=True,
        description="Декодировать ответы в строки"
    )
    socket_timeout: Optional[int] = Field(
        default=5,
        description="Таймаут сокета в секундах"
    )


class VectorDBSettings(BaseConfig):
    """
    Настройки векторной базы данных.
    """
    provider: str = Field(
        default="chroma",
        description="Провайдер векторной базы данных (chroma, pinecone, weaviate)"
    )
    host: str = Field(
        default="localhost",
        description="Хост векторной базы данных"
    )
    port: int = Field(
        default=8000,
        description="Порт векторной базы данных"
    )
    collection_name: str = Field(
        default="default_collection",
        description="Имя коллекции векторов"
    )
    embedding_dimension: int = Field(
        default=1536,
        description="Размерность эмбеддингов"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="API ключ для векторной базы данных"
    )


class DatabaseSettings(BaseConfig):
    """
    Общие настройки всех баз данных.
    """
    sqlite: SQLiteSettings = SQLiteSettings()
    redis: RedisSettings = RedisSettings()
    vector_db: VectorDBSettings = VectorDBSettings()
    
    # Флаги включения/отключения подсистем
    enable_sqlite: bool = Field(
        default=True,
        description="Включить подсистему SQLite"
    )
    enable_redis: bool = Field(
        default=True,
        description="Включить подсистему Redis"
    )
    enable_vector_db: bool = Field(
        default=True,
        description="Включить подсистему векторной БД"
    )