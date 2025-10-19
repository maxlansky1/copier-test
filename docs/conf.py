"""
Конфигурационный файл для сборщика документации Sphinx.

Этот файл содержит все настройки, необходимые для кастомизации входных и выходных данных Sphinx.
Он выполняется как код на Python во время сборки, при этом текущая директория устанавливается как директория конфигурации.
"""

import os
import sys

# Переменная окружения: флаг сборки документации
os.environ["SPHINX_BUILD"] = "1"

# Добавляет родительскую директорию в системный путь, чтобы Sphinx мог найти исходные модули
# Получаем путь к корню проекта и
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
template_path = os.path.join(project_root, "diagrams", "template")
icons_path = os.path.join(project_root, "diagrams", "icons")

sys.path.insert(0, project_root)

# Отладка для системного пути
# print(f"[DEBUG] Adding to sys.path: {project_root}")

# Информация о проекте для документации
project = "projectTemplate"
copyright = "2025, maxlansky"
author = "maxlansky"
release = "0.1"

# ============================================================================
# НАСТРОЙКИ ГЕНЕРАЦИИ UML-ДИАГРАММ (PlantUML)
# ============================================================================

# Настройки для работы с PlantUML и рендеринга UML-диаграмм.
# В GitHub Actions используется путь /usr/local/bin/plantuml/plantuml.jar, а для Windows — C:\\plantuml\\plantuml.jar.
if "GITHUB_ACTIONS" in os.environ:
    # Собираем полную команду: добавляем относительный путь, указываем относительные пути ко всем нужным файлам
    plantuml = f'java -jar "/usr/local/bin/plantuml/plantuml.jar" "{template_path}" "{icons_path}"'
elif os.name == "nt":  # Для Windows
    plantuml = (
        f'java -jar "C:\\plantuml\\plantuml.jar" -I"{template_path}" -I"{icons_path}"'
    )
else:
    raise OSError("Unsupported OS")

# Формат рендера диаграммы
plantuml_output_format = "svg_img"
plantuml_latex_output_format = "svg"


# ============================================================================
# РАСШИРЕНИЯ SPHINX
# ============================================================================

# Список расширений Sphinx
extensions = [
    # === Поддержка форматов ===
    "myst_parser",  # поддержка Markdown (.md)
    # === Автодокументация ===
    "sphinx.ext.autodoc",  # автодока из docstring'ов
    "sphinx.ext.viewcode",  # ссылки на исходники
    "sphinx.ext.napoleon",  # Google/NumPy стиль docstring'ов
    "sphinxcontrib.autodoc_pydantic",  # Улучшенная работа с Pydantic
    # === Утилиты и вспомогательные расширения ===
    "sphinx.ext.coverage",  # проверяет покрытие документации
    "sphinx_copybutton",  # добавляет кнопку скопировать код в документацию
    "sphinx_togglebutton",  # позволяет создавать разворачиваемые списки
    # === Визуализация и темы ===
    "sphinxcontrib.plantuml",  # добавляет поддержку plantuml
    "sphinx_immaterial",  # использовать тему mk docs
    # === GitHub Pages ===
    "sphinx.ext.githubpages",  # позволяет использовать стили sphinx при хостинге доков на github pages
]

# ============================================================================
# НАСТРОЙКИ АВТОДОКУМЕНТАЦИИ
# ============================================================================

# === Настройки autodoc ===
autodoc_default_options = {
    "members": True,  # Показывать публичные элементы
    "undoc-members": True,  # Показывать недокументированные члены (а не скрывать!)
    "private-members": False,  # Показывать приватные методы (_method) (а не скрывать!)
    "special-members": False,  # Показывать специальные методы (__init__, __str__) (а не скрывать!)
    "inherited-members": False,  # Показывать унаследованные методы
    "show-inheritance": True,  # Показывать иерархию наследования
    "exclude-members": "__weakref__",  # Исключить конкретные элементы
}

# Порядок элементов по исходному коду (естественнее для чтения)
autodoc_member_order = "bysource"
# Включать docstring класса + __init__ метода
autoclass_content = "both"
# Формат типов - короткий (чище выглядит)
# autodoc_typehints_format = "short"
# Отображение типов в описании (удобнее для чтения)
# autodoc_typehints = "description"

# === Настройки autodoc-pydantic ===
autodoc_pydantic_model_show_json = True
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_validator_summary = False
# autodoc_pydantic_model_erdantic_figure = True
# autodoc_pydantic_model_erdantic_figure_collapsed = True
autodoc_pydantic_field_list_validators = False


# === Настройки sphinx.ext.napoleon ===
napoleon_google_docstring = True
napoleon_numpy_docstring = False  # если используете только Google стиль
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_use_param = True

# === Настройки для myst_parser ===
myst_enable_extensions = [
    "amsmath",  # математика
    "colon_fence",  # ::: для блоков кода
    "deflist",  # определения
    "dollarmath",  # $...$ для математики
    "fieldlist",  # списки полей
    "html_admonition",  # HTML admonitions
    "html_image",  # HTML изображения
    "replacements",  # замены (c/o -> ©/®)
    "smartquotes",  # красивые кавычки
    "strikethrough",  # зачеркнутый текст
    "substitution",  # подстановки
    "tasklist",  # чекбоксы
]

# Автоматическое создание якорей на любой заголовок (7 уровней)
# TODO: продумать систему автоматической нумерации глав, разделов, диаграмм, таблиц, графиков итд
myst_heading_anchors = 7

# ============================================================================
# ОБРАБОТКА ИСХОДНЫХ ФАЙЛОВ
# ============================================================================

# Настройки для обработки исходных файлов, шаблонов, исключений и вывода HTML
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".git",  # игнорировать .git
    ".venv",  # виртуальное окружение
    "venv",  # альтернативный вариант
    ".env",  # файлы env
    "*.pyc",  # скомпилированные Python файлы
    "*~",  # временные файлы
]

language = "ru"


# ============================================================================
# НАСТРОЙКИ HTML-ТЕМЫ
# ============================================================================
# TODO: доделать кастомные настройки темы
# Настройки темы Mk Docs
html_theme = "sphinx_immaterial"
# material theme options (see theme.conf for more information)
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "site_url": "https://maxlansky1.github.io/projectTemplate",
    "repo_url": "https://github.com/maxlansky1/projectTemplate",
    "repo_name": "projectTemplate",
    "edit_uri": "blob/main/docs",
    "globaltoc_collapse": True,
    "features": [
        "navigation.expand",
        # "navigation.tabs",
        # "navigation.tabs.sticky",
        # "toc.integrate",
        "navigation.sections",
        # "navigation.instant",
        # "header.autohide",
        "navigation.top",
        "navigation.footer",
        # "navigation.tracking",
        # "search.highlight",
        "search.share",
        "search.suggest",
        "toc.follow",
        "toc.sticky",
        "content.tabs.link",
        "content.code.copy",
        "content.action.edit",
        "content.action.view",
        "content.tooltips",
        "announce.dismiss",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme)",
            "toggle": {
                "icon": "material/brightness-auto",
                "name": "Switch to light mode",
            },
        },
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "light-green",
            "accent": "light-blue",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "deep-orange",
            "accent": "lime",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to system preference",
            },
        },
    ],
    # BEGIN: version_dropdown
    "version_dropdown": True,
    "version_info": [
        {
            "version": "https://sphinx-immaterial.rtfd.io",
            "title": "ReadTheDocs",
            "aliases": [],
        },
        {
            "version": "https://jbms.github.io/sphinx-immaterial",
            "title": "Github Pages",
            "aliases": [],
        },
    ],
    # END: version_dropdown
    "toc_title_is_page_title": True,
    # BEGIN: social icons
    "social": [
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/jbms/sphinx-immaterial",
            "name": "Source on github.com",
        },
        {
            "icon": "fontawesome/brands/python",
            "link": "https://pypi.org/project/sphinx-immaterial/",
        },
    ],
    # END: social icons
}

# Настройки для истории изменений документации
html_context = {
    # === GitHub ===
    "github_user": "maxlansky",
    "github_repo": "projectTemplate",
    "github_version": "main",
    "display_github": True,
    # === Версии (только если реально планируешь версионирование) ===
    # 'current_version': release,  # автоматически из release
    # 'versions': {
    #     'latest': '/',  # текущая версия
    #     '0.1': '/0.1/',  # предыдущие версии
    # },
    # === Дополнительно (для Read the Docs и других хостингов) ===
    "source_type": "github",
    "source_user": "maxlansky",
    "source_repo": "projectTemplate",
    "source_version": "main",
    "source_suffix": ".rst",
}


# ============================================================================
# СТАТИЧЕСКИЕ ФАЙЛЫ (CSS, JS)
# ============================================================================

# Подключаем кастомные CSS и JS файлы
html_static_path = ["_static"]

html_js_files = [
    "custom.js",
]

html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    "custom.css",
]


# ============================================================================
# ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
# ============================================================================

# Дополнительная конфигурация sphinx-git (опционально)
git_untracked_check = False
git_remote_name = "origin"
git_branch = "main"  # или 'master', в зависимости от твоей ветки

# === Настройки sphinx-togglebutton ===

# Настройка CSS-селектора для элементов
togglebutton_selector = ".toggle, .admonition.dropdown"

# Настройка текста подсказки
togglebutton_hint = "Развернуть"
togglebutton_hint_hide = "Свернуть"

# Поведение при печати. По умолчанию True (разворачивает все элементы)
togglebutton_open_on_print = True
