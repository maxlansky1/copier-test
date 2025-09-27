"""
Настройки AI сервисов.

Этот модуль содержит конфигурацию для различных AI сервисов,
используемых в приложении: OpenRouter (LLM), AssemblyAI (STT),
ElevenLabs (TTS) и других будущих интеграций с искусственным интеллектом.
"""

from pydantic import Field, field_validator

from configs.schemas.base import BaseConfig
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OpenRouterSettings(BaseConfig):
    """
    Настройки OpenRouter API для работы с Large Language Models.

    OpenRouter - это платформа, предоставляющая доступ к различным
    LLM моделям от разных поставщиков через единый API. Содержит
    настройки для генерации текста, обработки изображений и управления
    параметрами запросов.
    """

    api_url: str = Field(
        default="https://openrouter.ai/api/v1/chat/completions",
        alias="OPENROUTER_API_URL",
        description=(
            "URL OpenRouter API для отправки запросов к моделям. "
            "Используется для всех операций с LLM: генерация текста, "
            "анализ изображений, обработка документов."
        ),
        examples=["https://openrouter.ai/api/v1/chat/completions"],
    )

    image_to_text_model: str = Field(
        default="meta-llama/llama-4-maverick:free",
        alias="OPENROUTER_IMAGE_TO_TEXT_MODEL",
        description=(
            "Модель для распознавания текста и анализа изображений. "
            "Используется для обработки изображений, отправленных в чат, "
            "и извлечения текстовой информации из визуального контента."
        ),
        examples=[
            "meta-llama/llama-4-maverick:free",
            "gpt-4-vision-preview",
            "claude-3-haiku",
        ],
    )

    model_name: str = Field(
        default="cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
        alias="MODEL_NAME",
        description=(
            "Основная модель для генерации текста и обработки запросов. "
            "Эта модель используется для большинства AI-операций: "
            "суммаризация, ответы на вопросы, генерация контента."
        ),
        examples=[
            "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            "openai/gpt-3.5-turbo",
            "anthropic/claude-3-sonnet",
            "google/gemini-pro",
        ],
    )

    max_retries: int = Field(
        default=3,
        alias="MAX_RETRIES",
        description=(
            "Максимальное количество попыток запроса при сетевых ошибках "
            "или временной недоступности API. Используется экспоненциальная "
            "задержка между попытками для предотвращения нагрузки на сервер."
        ),
        ge=1,
        le=10,
        examples=[1, 3, 5],
    )

    max_tokens: int = Field(
        default=400,
        alias="OPENROUTER_MAX_TOKENS",
        description=(
            "Максимальное количество токенов в ответе модели. "
            "Ограничивает длину генерируемого текста для экономии "
            "ресурсов и предотвращения чрезмерно длинных ответов."
        ),
        ge=1,
        le=4096,
        examples=[100, 400, 1000, 2000],
    )

    default_temperature: float = Field(
        default=0.55,
        alias="OPENROUTER_DEFAULT_TEMPERATURE",
        description=(
            "Температура генерации текста (0.0-2.0). "
            "Контролирует креативность ответов: "
            "0.0 = детерминированный, 1.0 = баланс, 2.0 = креативный. "
            "Низкие значения для точных ответов, высокие для креатива."
        ),
        ge=0.0,
        le=2.0,
        examples=[0.0, 0.55, 1.0, 1.5, 2.0],
    )

    top_p: float = Field(
        default=0.85,
        alias="OPENROUTER_TOP_P",
        description=(
            "Top-P (nucleus) sampling - вероятностный порог для выбора токенов. "
            "Ограничивает выбор токенов до тех пор, пока их совокупная "
            "вероятность не достигнет этого значения. Помогает балансировать "
            "между разнообразием и качеством генерации."
        ),
        ge=0.0,
        le=1.0,
        examples=[0.1, 0.5, 0.85, 0.95],
    )

    frequency_penalty: float = Field(
        default=0.8,
        alias="OPENROUTER_FREQUENCY_PENALTY",
        description=(
            "Штраф за частоту повторения токенов (0.0-2.0). "
            "Уменьшает вероятность повторения уже использованных слов "
            "и фраз. Положительные значения поощряют разнообразие, "
            "отрицательные - повторение."
        ),
        ge=0.0,
        le=2.0,
        examples=[0.0, 0.8, 1.0, 1.5],
    )

    presence_penalty: float = Field(
        default=0.7,
        alias="OPENROUTER_PRESENCE_PENALTY",
        description=(
            "Штраф за присутствие токенов в контексте (0.0-2.0). "
            "Поощряет появление новых тем и концепций в ответе. "
            "Высокие значения делают ответы более разнообразными, "
            "низкие - более фокусированными на исходной теме."
        ),
        ge=0.0,
        le=2.0,
        examples=[0.0, 0.7, 1.0, 1.2],
    )

    @field_validator("api_url")
    @classmethod
    def validate_api_url(cls, v: str) -> str:
        """
        Валидация URL API OpenRouter.

        Проверяет, что URL начинается с правильного протокола
        (http:// или https://) и удаляет завершающие пробелы и слэши.

        Args:
            v: URL для валидации

        Returns:
            str: Валидный URL без завершающих символов

        Raises:
            ValueError: Если URL не начинается с http:// или https://

        Examples:
            >>> cls.validate_api_url("https://openrouter.ai/api/v1/chat/completions  ")
            'https://openrouter.ai/api/v1/chat/completions'

            >>> cls.validate_api_url("openrouter.ai/api")
            ValueError: API URL должен начинаться с http:// или https://
        """
        if not v.startswith(("http://", "https://")):
            raise ValueError("API URL должен начинаться с http:// или https://")
        return v.strip().rstrip("/")


class AssemblyAISettings(BaseConfig):
    """
    Настройки AssemblyAI для распознавания речи (Speech-to-Text).

    AssemblyAI - сервис для преобразования аудио в текст с поддержкой
    различных языков, диалектов и специализированных моделей распознавания.
    """

    api_key: str = Field(
        default="",
        alias="ASSEMBLYAI_API_KEY",
        description=(
            "API ключ для AssemblyAI. Необходим для доступа к "
            "сервисам распознавания речи и обработки аудио. "
            "Если не задан, функции STT будут недоступны."
        ),
        examples=["1234567890abcdef1234567890abcdef"],
    )

    @property
    def is_configured(self) -> bool:
        """
        Проверка, что сервис AssemblyAI настроен и готов к использованию.

        Returns:
            bool: True если API ключ задан и не пустой, False в противном случае

        Examples:
            >>> settings = AssemblyAISettings(api_key="valid_key")
            >>> settings.is_configured
            True

            >>> settings = AssemblyAISettings(api_key="")
            >>> settings.is_configured
            False
        """
        return bool(self.api_key and self.api_key.strip())


class ElevenLabsSettings(BaseConfig):
    """
    Настройки ElevenLabs для синтеза речи (Text-to-Speech).

    ElevenLabs - сервис для преобразования текста в естественную речь
    с использованием различных голосов и настроек интонации.
    """

    api_key: str = Field(
        default="",
        alias="ELEVENLABS_API_KEY",
        description=(
            "API ключ для ElevenLabs. Необходим для доступа к "
            "сервисам синтеза речи и управления голосами. "
            "Если не задан, функции TTS будут недоступны."
        ),
        examples=["1234567890abcdef1234567890abcdef"],
    )

    @property
    def is_configured(self) -> bool:
        """
        Проверка, что сервис ElevenLabs настроен и готов к использованию.

        Returns:
            bool: True если API ключ задан и не пустой, False в противном случае

        Examples:
            >>> settings = ElevenLabsSettings(api_key="valid_key")
            >>> settings.is_configured
            True

            >>> settings = ElevenLabsSettings(api_key="")
            >>> settings.is_configured
            False
        """
        return bool(self.api_key and self.api_key.strip())


logger.debug("Модели конфигурации AI сервисов загружены")
