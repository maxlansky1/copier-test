# Справочник SQL

Этот справочник предоставляет информацию об API (классы, методы, функции, атрибуты) модулей, отвечающих за взаимодействие с базой данных в проекте, включая конфигурацию, ORM-модели, доступ к данным (DAO) и инструменты миграции (Alembic).

## Конфигурация

### Основные настройки

```{eval-rst}
.. autopydantic_model:: configs.settings.AppSettings
```

### Схемы БД

```{eval-rst}
.. autopydantic_model:: configs.schemas.database.SQLiteSettings
```

## SQLAlchemy (Core/Models)

### Core (Движок, Сессия, Декоратор)

```{eval-rst}
.. automodule:: src.databases.sqlite.core
```

### Базовая модель

```{eval-rst}
.. literalinclude:: ../../src/databases/sqlite/models/base.py
   :language: python
   :caption: Базовая модель SQLAlchemy
```

### Модель User

```{eval-rst}
.. literalinclude:: ../../src/databases/sqlite/models/user.py
   :language: python
   :caption: Модель пользователя
```

## Схемы (Pydantic)

### Схемы User

```{eval-rst}
.. literalinclude:: ../../src/databases/sqlite/schemas/user.py
   :language: python
   :caption: Схемы пользователя
```

## Доступ к данным (DAO)

### Базовый DAO

```{eval-rst}
.. literalinclude:: ../../src/databases/dao/base.py
   :language: python
   :caption: Базовый DAO
```

### DAO User

```{eval-rst}
.. literalinclude:: ../../src/databases/dao/user_dao.py
   :language: python
   :caption: DAO для модели User
```

## Alembic

Alembic — это инструмент управления миграциями базы данных для SQLAlchemy. В проекте используется асинхронная конфигурация для работы с SQLite.

### Структура директории Alembic

```{code-block} text
alembic/
├── README
├── env.py          # Скрипт настройки окружения Alembic
├── script.py.mako  # Шаблон для генерации файлов миграций
└── versions/       # Директория с файлами миграций
alembic.ini         # основная конфигурация Alembic
```

### alembic.ini

Файл `.\alembic.ini` находится в **корне проекта** и содержит основную конфигурацию для Alembic, включая расположение скриптов, настройки пути Python и логирования. URL базы данных задаётся в `env.py`, но может быть определён и здесь.

```{eval-rst}
.. literalinclude:: ../../alembic.ini
   :language: text
   :caption: alembic.ini
```

#### Секция `[alembic]`

*   `script_location`: Указывает путь к директории с миграциями относительно `alembic.ini`. В данном случае: `%(here)s/alembic`, что означает `./alembic`.
*   `prepend_sys_path`: Список путей, которые будут добавлены в `sys.path`. Установлено в `.` (текущая директория), чтобы Python мог импортировать модули проекта, включая `env.py`.
*   `path_separator`: Разделитель для списков путей в `ini` файле. Установлено в `os`, что означает использование системного разделителя (`:` на Unix, `;` на Windows).
*   `sqlalchemy.url`: URL подключения к базе данных. В данном случае он задаётся в `env.py`, но может быть определён здесь. Используется только `env.py`.

#### Секция `[post_write_hooks]`

Позволяет определять скрипты или функции Python, которые будут запускаться на вновь сгенерированных файлах миграций (например, для форматирования или линтинга). В текущем `alembic.ini` закомментированы примеры для `black` и `ruff`.

#### Секции логирования

Секции `[loggers]`, `[handlers]`, `[formatters]` и `[logger_*]` определяют настройки логирования для Alembic и SQLAlchemy. Используется `StreamHandler` для вывода в `stderr`.

### env.py

`env.py` является **центральным элементом** настройки окружения Alembic. Он отвечает за загрузку конфигурации, подключение к базе данных и выполнение миграций.

```{eval-rst}
.. literalinclude:: ../../alembic/env.py
   :language: python
   :caption: env.py
```

```{question} Зачем нужен комментарий # noqa: F401 при импорте модели?
Комментарий `# noqa: F401` используется, чтобы линтеры, например Ruff, **не удаляли импорт модели**, который кажется им неиспользуемым.

В коде модуля модель напрямую не вызывается, поэтому линтер считает импорт лишним и может **автоматически удалить его** при проверке.
Однако этот импорт **обязателен для работы Alembic**: Alembic сканирует `Base.metadata`, чтобы найти все модели и корректно построить миграции.

Добавляя `# noqa`, мы сообщаем Ruff: «Не трогай эту строку — она нужна для Alembic», предотвращая удаление важного импорта и сохраняя корректность миграций.

Подробнее о правилах форматирования читайте в [документации ruff](https://docs.astral.sh/ruff/rules/)
```
