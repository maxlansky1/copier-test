"""
Пакет схем конфигурации Pydantic.
"""

from src.utils.logger import get_logger

from .ai import AssemblyAISettings, ElevenLabsSettings, OpenRouterSettings
from .base import BaseConfig
from .file_processing import MediaProcessingSettings
from .storage import StorageSettings  # noqa: F401
from .telegram import TelegramSettings  # noqa: F401

logger = get_logger(__name__)

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
    "SQLiteSettings",
]

logger.debug("Конфигурационные модели загружены")
