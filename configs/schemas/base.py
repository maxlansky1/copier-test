"""
Базовая модель конфигурации с поддержкой .env файлов.

Этот модуль предоставляет основу для всех конфигурационных классов
в приложении. Он автоматически загружает переменные окружения из
.env файлов и обеспечивает базовую валидацию данных.
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.logger import get_logger

logger = get_logger(__name__)


class BaseConfig(BaseSettings):
    """
    Базовая конфигурация с поддержкой .env файлов.

    Наследуется всеми конфигурационными классами приложения.
    Автоматически загружает переменные окружения и применяет
    универсальные валидаторы для очистки данных.
    """

    model_config = SettingsConfigDict(
        env_file=".env",  # Автоматическая загрузка .env
        env_file_encoding="utf-8",  # Кодировка
        case_sensitive=False,  # Регистронезависимость
        extra="ignore",  # Игнорировать неизвестные переменные
    )

    @field_validator("*", mode="before")
    @classmethod
    def strip_string_fields(cls, v):
        """
        Универсальный валидатор для очистки строк.

        Удаляет ведущие и завершающие пробелы из всех строковых значений
        перед их обработкой. Это помогает избежать ошибок из-за лишних
        пробелов в переменных окружения.

        Args:
            v: Значение поля для валидации

        Returns:
            Очищенное значение или оригинальное значение для не-строк
        """
        if isinstance(v, str):
            return v.strip()
        return v


logger.debug("Базовая модель конфигурации загружена")
