"""
Настройки хранилища и путей.

Этот модуль содержит базовые настройки для работы с файловой системой,
включая корневую директорию проекта и параметры хранения данных.
"""

from pathlib import Path

from pydantic import BaseModel, Field


class StorageSettings(BaseModel):
    """
    Настройки хранилища и путей.

    Содержит базовые параметры для работы с файловой системой приложения.
    Основной фокус на корневой директории проекта, от которой вычисляются
    все остальные пути. Остальные директории определяются вручную через Path.
    """

    project_root: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent,
        description=(
            "Корневая директория проекта. Используется как базовый путь "
            "для вычисления всех остальных директорий приложения."
        ),
    )

    data_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent / "data",
        description=("Директория для хранения данных (включая БД)"),
    )
