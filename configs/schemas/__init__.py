"""
Инициализация моделей конфигурации
"""

from ai import AssemblyAISettings, ElevenLabsSettings, OpenRouterSettings
from base import BaseConfig
from file_processing import MediaProcessingSettings
from storage import StorageSettings
from telegram import TelegramSettings

from src.utils.logger import get_logger

logger = get_logger(__name__)

__all__ = [
    "BaseConfig",
    "TelegramSettings",
    "OpenRouterSettings",
    "AssemblyAISettings",
    "ElevenLabsSettings",
    "StorageSettings",
    "MediaProcessingSettings",
]

logger.debug("Конфигурационные модели загружены")
