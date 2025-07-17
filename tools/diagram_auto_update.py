"""Модуль для автоматического обновления диаграммы зависимостей.

Скрипт анализирует новые файлы в репозитории и генерирует PlantUML диаграмму,
отображающую структуру проекта с возможностью перехода к файлам через vscode:// ссылки.
"""

import subprocess  # nosec B404
from pathlib import Path

# Пути к корневой директории исходного кода и директории с диаграммами
BASE_DIR = Path(__file__).parent.parent.resolve()
SRC_DIR = BASE_DIR / "src"
DIAGRAMS_DIR = BASE_DIR / "diagrams"
OUTPUT_FILE = DIAGRAMS_DIR / "temp_containers.puml"

# Настройки отображения для файлов по расширениям:
# (Человеческое имя типа файла, имя спрайта PlantUML, тег в диаграмме)
EXT_SETTINGS = {
    ".py": ("Python", "python", "code"),
    ".js": ("JavaScript", "javascript", "code"),
    ".ts": ("TypeScript", "typescript", "code"),
    ".json": ("JSON", "json", "config"),
    ".yaml": ("YAML", "yaml", "config"),
    ".yml": ("YAML", "yaml", "config"),
    ".txt": ("Text", "text", "docs"),
    ".md": ("Markdown", "markdown", "docs"),
    ".ipynb": ("Notebook", "jupyter", "notebook"),
    ".html": ("HTML", "html", "web"),
    ".css": ("CSS", "css", "web"),
}


def get_changed_files():
    """Получает список новых (неотслеживаемых) файлов в репозитории Git.

    Returns:
        List[str]: Список относительных путей к новым файлам.

    Note:
        Использует `git ls-files --others --exclude-standard` для получения списка файлов.
        Валидация пути выполняется в вызывающем коде.
    """
    try:
        result = subprocess.run(  # nosec B603, B607
            ["git", "ls-files", "--others", "--exclude-standard"],
            stdout=subprocess.PIPE,
            text=True,
            cwd=BASE_DIR,
            check=True,
        )
        files = [
            line.strip() for line in result.stdout.strip().split("\n") if line.strip()
        ]
        return files
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        return []


def build_container_definitions(added_files):
    """Обрабатывает список добавленных файлов и возвращает определения для диаграммы.

    Args:
        added_files (List[str]): Список относительных путей к добавленным файлам.

    Returns:
        Tuple[List[str], Dict]: Кортеж содержащий:
            - Список строк с определениями vscode-ссылок
            - Словарь с иерархией папок и файлов для генерации PlantUML
    """
    defines = []
    boundaries = {}

    for filepath in added_files:
        full_path = BASE_DIR / filepath

        # Фильтруем только файлы внутри src, которые реально существуют
        if not filepath.startswith("src/") or not full_path.exists():
            continue

        # Игнорируем служебные файлы Python
        if full_path.name == "__init__.py":
            continue

        ext = full_path.suffix.lower()
        file_type, sprite, tag = EXT_SETTINGS.get(ext, ("File", "file", "other"))

        # Получаем относительный путь от корня проекта
        rel_path = full_path.relative_to(BASE_DIR)
        parts = rel_path.parts  # ('src', 'subdir', 'file.py')

        # Формируем уникальный идентификатор и vscode-ссылку (без жёсткого C:/)
        var_name = (full_path.stem + "_" + ext.lstrip(".")).lower()
        var_const = var_name.upper()
        vscode_link = f"vscode://file/{rel_path.as_posix()}"
        defines.append(f'!define {var_const} "{vscode_link}"')

        # Строим иерархию папок: src/.../папка/файл
        current = boundaries
        for part in parts[1:-1]:  # пропускаем "src", идём по папкам
            current = current.setdefault(part, {})
        current.setdefault("files", []).append(
            (parts[-1], var_name, file_type, sprite, tag, var_const)
        )

    return defines, boundaries


def write_container_block(f, name, content, indent=0):
    """Рекурсивно записывает блок Container_Boundary и файлы внутри него.

    Args:
        f: Файловый объект для записи.
        name (str): Имя текущего контейнера.
        content (Dict): Содержимое контейнера (подпапки и файлы).
        indent (int): Уровень отступа для форматирования.
    """
    space = " " * indent

    # Записываем файлы в текущей папке
    if "files" in content:
        for filename, var_name, file_type, sprite, tag, var_const in content["files"]:
            f.write(
                f'{space}    Container({var_name}, "{filename}", "{file_type}", '
                f'"{filename}", $tags="{tag}", $sprite="{sprite}", '
                f'$link="{var_const}")\n'
            )

    # Рекурсивно обрабатываем подпапки
    for subfolder, subcontent in content.items():
        if subfolder == "files":
            continue
        f.write(
            f'{space}    Container_Boundary({subfolder}, "{subfolder}", $tags="code") {{\n'
        )
        write_container_block(f, subfolder, subcontent, indent + 4)
        f.write(f"{space}    }}\n")


def write_temp_puml(defines, boundaries):
    """Генерирует временный .puml файл с определениями ссылок и иерархией компонентов.

    Args:
        defines (List[str]): Список определений vscode-ссылок.
        boundaries (Dict): Иерархия папок и файлов проекта.
    """
    DIAGRAMS_DIR.mkdir(exist_ok=True)  # Создаём папку, если нет

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("@startuml\n\n")

        # Вставляем все !define ссылки
        for line in defines:
            f.write(line + "\n")

        f.write('\nContainer_Boundary(src, "src (исходный код)", $tags="code") {\n')
        write_container_block(f, "src", boundaries, indent=4)
        f.write("}\n\n@enduml\n")


if __name__ == "__main__":
    """Основная точка входа скрипта."""
    added_files = get_changed_files()
    print("Changed files detected:", added_files)  # Для отладки

    defines, boundaries = build_container_definitions(added_files)
    write_temp_puml(defines, boundaries)

    print(f"Generated PlantUML diagram at {OUTPUT_FILE}")
