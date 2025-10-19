"""
Настройки Telegram бота.

Этот модуль содержит конфигурацию для работы с Telegram API,
включая токен бота, список администраторов и другие параметры
для взаимодействия с мессенджером.
"""

from typing import List, Optional

from pydantic import Field, field_validator

from configs.schemas.base import BaseConfig
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TelegramSettings(BaseConfig):
    """
    Настройки Telegram бота.

    Содержит все необходимые параметры для инициализации и работы
    Telegram бота, включая аутентификационные данные и параметры
    безопасности. Обеспечивает валидацию и парсинг конфигурационных
    параметров из переменных окружения.
    """

    token: str = Field(
        default="1234567890",
        alias="TELEGRAM_BOT_TOKEN",
        description=(
            "Токен Telegram бота для аутентификации в Telegram Bot API. "
            "Обязательный параметр для работы бота."
        ),
        min_length=1,
        examples=["123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ-123456789"],
    )

    chat_id: Optional[str] = Field(
        default="",
        alias="TELEGRAM_CHAT_ID",
        description=(
            "ID чата для отправки системных уведомлений и логов. "
            "Если не указан, уведомления будут отправляться в приватные чаты с пользователями."
        ),
        examples=["-1001234567890", "123456789"],
    )

    admin_ids: List[int] = Field(
        default_factory=list,
        alias="TELEGRAM_ADMIN_IDS",
        description=(
            "Список ID администраторов бота с расширенными правами. "
            "Администраторы могут использовать специальные команды и получать "
            "доступ к системной информации."
        ),
        examples=[[123456789, 987654321]],
    )

    @field_validator("admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, v) -> List[int]:
        """
        Парсинг списка ID администраторов из различных форматов.

        Поддерживает несколько форматов входных данных:
        - Строка с разделителями-запятыми: "123456789,987654321"
        - Список строк: ["123456789", "987654321"]
        - Список целых чисел: [123456789, 987654321]
        - Пустая строка или None: возвращает пустой список

        Args:
            v: Входное значение в различных форматах

        Returns:
            List[int]: Список ID администраторов в виде целых чисел

        Raises:
            ValueError: Если строку невозможно преобразовать в числа

        Examples:
            >>> cls.parse_admin_ids("123456789,987654321")
            [123456789, 987654321]

            >>> cls.parse_admin_ids(["123456789", "987654321"])
            [123456789, 987654321]

            >>> cls.parse_admin_ids("")
            []
        """
        if isinstance(v, str):
            if not v.strip():
                return []
            try:
                # Разбиваем строку по запятым и преобразуем в int
                return [int(x.strip()) for x in v.split(",") if x.strip()]
            except ValueError as e:
                raise ValueError(
                    f"Неверный формат ID администраторов. "
                    f"Ожидались целые числа, разделенные запятыми. "
                    f"Получено: {v}"
                ) from e
        elif isinstance(v, list):
            # Преобразуем список в список целых чисел
            return [int(x) for x in v]
        # Для всех остальных случаев возвращаем пустой список
        return []

    @property
    def is_configured(self) -> bool:
        """
        Проверка, что бот настроен и готов к работе.

        Returns:
            bool: True если бот настроен и готов к работе, False в противном случае
        """
        return bool(self.token and self.token.strip())


logger.debug("Модель конфигурации Telegram загружена")
