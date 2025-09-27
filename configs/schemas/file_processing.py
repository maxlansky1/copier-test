"""
Настройки обработки медиафайлов.

Этот модуль содержит конфигурацию для скачивания и обработки
медиафайлов различных типов: видео, аудио, изображения, документы.
"""

from pydantic import Field

from configs.schemas.base import BaseConfig
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MediaProcessingSettings(BaseConfig):
    """
    Настройки обработки медиафайлов.

    Содержит параметры для управления процессом скачивания и обработки
    медиафайлов, включая ограничения по размеру, количество попыток
    скачивания и временные задержки между попытками.
    """

    download_max_file_size: int = Field(
        default=50 * 1024 * 1024,  # 50 MB
        alias="DOWNLOAD_MAX_FILE_SIZE",
        description=(
            "Максимальный размер файла для скачивания в байтах. "
            "Файлы больше этого размера будут отклонены для предотвращения "
            "перерасхода дискового пространства и памяти."
        ),
        gt=0,
        examples=[52428800, 104857600, 209715200],  # 50MB, 100MB, 200MB
    )

    download_max_retries: int = Field(
        default=3,
        alias="DOWNLOAD_MAX_RETRIES",
        description=(
            "Максимальное количество попыток скачивания файла при ошибках. "
            "Используется экспоненциальная задержка между попытками "
            "для предотвращения нагрузки на сервер."
        ),
        ge=1,
        le=10,
        examples=[1, 3, 5, 10],
    )

    download_retry_delay: int = Field(
        default=2,
        alias="DOWNLOAD_RETRY_DELAY",
        description=(
            "Базовая задержка между попытками скачивания в секундах. "
            "Фактическая задержка увеличивается экспоненциально: "
            "delay * (2 ^ attempt_number)"
        ),
        ge=0,
        examples=[0, 1, 2, 5, 10],
    )


logger.debug("Модели конфигурации обработки медиафайлов загружены")
