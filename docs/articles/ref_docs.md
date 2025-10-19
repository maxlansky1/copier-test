# `docs/`

Этот документ предоставляет справочную информацию о конфигурационных файлах, используемых для сборки документации с помощью Sphinx и MyST Parser в проекте.

## `index.rst`

`index.rst` - **главный входной файл** для документации Sphinx, определяющий **структуру и навигацию** между документами.

```{eval-rst}
.. toggle:: Показать

   .. literalinclude:: ../../docs/index.rst
      :language: rst
      :caption: index.rst
```

### Назначение

*   **Точка входа:** Sphinx начинает сборку документации с этого файла. Он определяет, какие документы включены в проект и как они связаны между собой.
*   **Сборка:** Файл `index.rst` содержит директиву `toctree`, которая "собирает" все указанные в ней исходные файлы (включая `*.md`, обрабатываемые через `myst_parser`) в единую иерархическую структуру HTML-страниц.
*   **Навигация:** На основе содержимого `index.rst` (в частности, `toctree`) генерируется основное оглавление и навигационное меню для HTML-документации.

## Makefile

`Makefile` автоматизирует процесс локальной сборки документации Sphinx в Unix-подобных системах (Linux, macOS).

```{eval-rst}
.. toggle:: Показать

   .. literalinclude:: ../../docs/Makefile
      :language: make
      :caption: Makefile
```

### Переменные

*   `SPHINXOPTS`: Дополнительные опции для `sphinx-build`. По умолчанию пусто (`?=` означает, что переменная может быть переопределена извне).
*   `SPHINXBUILD`: Команда для вызова `sphinx-build`. По умолчанию `sphinx-build`.
*   `SOURCEDIR`: Директория с исходными файлами документации. Установлено в `.` (текущая директория, т.е. `docs`).
*   `BUILDDIR`: Директория, куда будет собрана документация. Установлено в `_build`.

### Цели (Targets)

*   `help`: Выводит справку по доступным целям `sphinx-build`.
*   `clean`: Удаляет содержимое `BUILDDIR`, очищая кэш и результаты предыдущих сборок.
*   `html`: Запускает `sphinx-build` для генерации HTML-документации в `$(BUILDDIR)/html`.
*   `livehtml`: Использует `sphinx-autobuild` для запуска сервера разработки с автоматической перезагрузкой при изменении файлов. Открывает браузер. Порт выбирается автоматически.

## make.bat

`make.bat` - скрипт командной строки Windows, эквивалентный `Makefile`, обеспечивающий автоматизацию сборки документации Sphinx в Windows.

```{eval-rst}
.. toggle:: Показать

   .. literalinclude:: ../../docs/make.bat
      :language: cmd
      :caption: make.bat
```

### Переменные

*   `SPHINXBUILD`: Команда для вызова `sphinx-build`. Если не установлена, по умолчанию используется `sphinx-build`.
*   `SOURCEDIR`: Директория с исходными файлами документации. Установлено в `.` (текущая директория, т.е. `docs`).
*   `BUILDDIR`: Директория, куда будет собрана документация. Установлено в `_build`.

### Функциональность

*   Проверяет наличие `sphinx-build` в PATH. Если не находит, выводит сообщение об ошибке и инструкции по установке.
*   Проверяет наличие `sphinx-autobuild` при вызове цели `livehtml`. Если не находит, выводит сообщение об ошибке.
*   Обрабатывает переданный аргумент (например, `html`, `clean`, `livehtml`) и вызывает соответствующую команду `sphinx-build` или `sphinx-autobuild`.
*   Цель `help` вызывает `sphinx-build -M help` для отображения справки.

## conf.py

`conf.py` - основной **конфигурационный файл Sphinx**, написанный на Python. Он выполняется во время сборки и определяет все настройки документации.

```{eval-rst}
.. toggle:: Показать

   .. literalinclude:: ../../docs/conf.py
      :language: python
      :caption: conf.py
```

### Информация о проекте

*   `project`: Имя проекта
*   `copyright`: Информация об авторских правах
*   `author`: Имя автора
*   `release`: Полная версия проекта

### Настройки генерации UML-диаграмм (PlantUML)

*   `plantuml`: Команда для вызова исполняемого файла PlantUML. Настройка отличается в зависимости от операционной системы (Windows или GitHub Actions) и включает пути к шаблонам (`template_path`) и иконкам (`icons_path`) для C4 диаграмм.
*   `plantuml_output_format`: Формат вывода диаграмм. Установлен в `"svg_img"`.
*   `plantuml_latex_output_format`: Формат вывода диаграмм для LaTeX. Установлен в `"svg"`.

### Расширения Sphinx

Список `extensions` включает используемые расширения Sphinx:

*   `myst_parser`: Поддержка формата MyST Markdown (`.md`).
*   `sphinx.ext.autodoc`: Автодокументация из docstring'ов Python-кода.
*   `sphinx.ext.viewcode`: Ссылки на исходный код в документации.
*   `sphinx.ext.napoleon`: Поддержка docstring'ов в формате Google и NumPy.
*   `sphinx.ext.coverage`: Проверка покрытия документацией.
*   `sphinx_copybutton`: Добавляет кнопку "копировать" к блокам кода.
*   `sphinx_togglebutton`: Позволяет создавать разворачиваемые блоки.
*   `sphinxcontrib.plantuml`: Поддержка PlantUML диаграмм.
*   `sphinx_immaterial`: Используемая HTML-тема (аналог Material for MkDocs).
*   `sphinx.ext.githubpages`: Помогает при хостинге документации на GitHub Pages.

### Настройки автодокументации

*   `autodoc_default_options`: Определяет, какие элементы Python-кода (members, undoc-members, private-members, special-members, inherited-members) включать в автодокументацию, а также настройки отображения (например, `show-inheritance`, `exclude-members`).
*   `autodoc_member_order`: Порядок отображения элементов. Установлен в `"bysource"` (по порядку в исходном коде).
*   `autoclass_content`: Что включать в документацию класса. Установлено в `"both"` (и docstring класса, и метод `__init__`).
*   `autodoc_typehints_format`: Формат отображения аннотаций типов. Установлен в `"short"`.
*   `autodoc_typehints`: Где отображать аннотации типов. Установлено в `"description"` (в описании).
*   `napoleon_*`: Настройки для расширения Napoleon (Google/NumPy docstrings).

### Настройки MyST Parser

*   `myst_enable_extensions`: Список расширений MyST, включающих поддержку математики (`amsmath`, `dollarmath`), списков определений (`deflist`), зачеркивания (`strikethrough`), чекбоксов (`tasklist`) и т.д.
*   `myst_heading_anchors`: Уровень заголовков, для которых автоматически создаются якоря (ссылки). Установлено в `7`.

### Обработка исходных файлов

*   `source_suffix`: Сопоставление расширений файлов с их типами (`.rst` -> `restructuredtext`, `.md` -> `markdown`).
*   `templates_path`: Список директорий для поиска HTML-шаблонов Sphinx. Установлено в `["_templates"]`.
*   `exclude_patterns`: Список шаблонов имён файлов/директорий, которые будут исключены из сборки (например, `_build`, `.git`, `.venv`).
*   `language`: Язык документации. Установлен в `"ru"` (русский).

### Настройки HTML-темы (sphinx_immaterial)

*   `html_theme`: Выбранная тема. Установлена в `"sphinx_immaterial"`.
*   `html_theme_options`: Словарь с настройками темы, включая иконки, URL-адреса репозитория, функции навигации (`features`), цветовые схемы (`palette`), настройки версионирования (`version_dropdown`), социальные иконки (`social`) и т.д.
*   `html_context`: Контекстные переменные, часто используемые в шаблонах. Включают настройки для отображения ссылок на GitHub (`display_github`, `github_*`).

### Статические файлы

*   `html_static_path`: Список директорий для поиска статических файлов (CSS, JS, изображения). Установлено в `["_static"]`.
*   `html_js_files`: Список JS-файлов, которые будут включены в HTML.
*   `html_css_files`: Список CSS-файлов, которые будут включены в HTML (включая внешние, например, Font Awesome).

### Дополнительные настройки

*   `git_*`: Настройки для расширения, связанного с Git (например, `sphinx-git`).
*   `togglebutton_*`: Настройки для расширения `sphinx-togglebutton`.