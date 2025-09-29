"""
Пакет схем конфигурации Pydantic.
"""

from .ai import (
    AssemblyAISettings,
    ElevenLabsSettings,
    OpenRouterSettings,
)
from .base import BaseConfig
from .database import (
    DatabaseSettings,
    SQLiteSettings,
    RedisSettings,
    VectorDBSettings,
)
from .file_processing import MediaProcessingSettings
from .storage import StorageSettings
from .telegram import TelegramSettings

__all__ = [
    # AI
    "AssemblyAISettings",
    "ElevenLabsSettings", 
    "OpenRouterSettings",
    # Base
    "BaseConfig",
    # Database
    "DatabaseSettings",
    "SQLiteSettings",
    "RedisSettings", 
    "VectorDBSettings",
    # File Processing
    "MediaProcessingSettings",
    # Storage
    "StorageSettings",
    # Telegram
    "TelegramSettings",
]