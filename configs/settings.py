"""
Основная конфигурация приложения с использованием Pydantic 2.
"""

from typing import ClassVar, Optional

from configs.schemas.ai import (
    AssemblyAISettings,
    ElevenLabsSettings,
    OpenRouterSettings,
)
from configs.schemas.base import BaseConfig
from configs.schemas.database import DatabaseSettings
from configs.schemas.file_processing import MediaProcessingSettings
from configs.schemas.storage import StorageSettings
from configs.schemas.telegram import TelegramSettings
from src.utils.logger import get_logger

# Создаем логгер для конфигурации
logger = get_logger(__name__)


class AppSettings(BaseConfig):
    """
    Основная конфигурация приложения.
    """

    # Вложенные настройки для структурированного доступа
    telegram: TelegramSettings = TelegramSettings()
    openrouter: OpenRouterSettings = OpenRouterSettings()
    assemblyai: AssemblyAISettings = AssemblyAISettings()
    elevenlabs: ElevenLabsSettings = ElevenLabsSettings()
    storage: StorageSettings = StorageSettings()
    database: DatabaseSettings = DatabaseSettings()  # Новые настройки БД
    file_processing: MediaProcessingSettings = MediaProcessingSettings()

    # Синглтон для производительности и консистентности
    _instance: ClassVar[Optional["AppSettings"]] = None

    def __init__(self, **data):
        """Инициализация с логированием безопасной конфигурации."""
        super().__init__(**data)
        # Логируем безопасный дамп при создании
        self._log_safe_configuration()

    def _log_safe_configuration(self):
        """Логирование безопасной конфигурации при инициализации."""
        try:
            safe_dump = self.get_safe_dump()
            logger.info("🔧 Конфигурация приложения загружена")
            logger.debug(f"Настройки: {safe_dump}")
        except Exception as e:
            logger.warning(f"Не удалось залогировать конфигурацию: {e}")

    @classmethod
    def get_instance(cls) -> "AppSettings":
        """Получить синглтон экземпляр конфигурации."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def is_fully_configured(self) -> bool:
        """Проверка полной конфигурации приложения."""
        return self.telegram.is_configured and bool(
            self.openrouter.model_name and self.openrouter.model_name.strip()
        )

    def get_safe_dump(self) -> dict:
        """Получить безопасный дамп всех настроек для логирования."""
        dump = self.model_dump()

        # Удаляем чувствительные данные
        sensitive_keys = [
            "token",
            "api_key",
            "TELEGRAM_BOT_TOKEN",
            "ASSEMBLYAI_API_KEY",
            "ELEVENLABS_API_KEY",
            "password",  # Добавляем пароли
        ]

        def sanitize_dict(d: dict) -> dict:
            """Рекурсивно очищает словарь от чувствительных данных."""
            result = {}
            for key, value in d.items():
                if any(
                    sensitive_key.lower() in key.lower()
                    for sensitive_key in sensitive_keys
                ):
                    result[key] = "***"
                elif isinstance(value, dict):
                    result[key] = sanitize_dict(value)
                else:
                    result[key] = value
            return result

        return sanitize_dict(dump)


# Создаем экземпляр для импорта
settings = AppSettings.get_instance()