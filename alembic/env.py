"""
Модуль конфигурации Alembic для управления миграциями базы данных.

Использует SQLAlchemy и асинхронный движок для применения миграций в
офлайн- и онлайн-режимах. Подключается к SQLite через настройки проекта
и использует декларативные модели из `Base`.

Основные функции:
- run_migrations_offline: выполнение миграций без подключения к БД.
- run_migrations_online: выполнение миграций с подключением к БД.
- run_async_migrations: асинхронный запуск миграций.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from configs.settings import settings
from src.databases.sqlite.models.base import Base
from src.databases.sqlite.models.user import User  # noqa: F401

# TODO: добавить миграции алембик в CI/CD

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем URL подключения
config.set_main_option("sqlalchemy.url", settings.database.sqlite.database_url)

# add your model's MetaData object here
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Запуск миграций в офлайн-режиме.

    Контекст настраивается только с URL без создания движка,
    хотя движок также допустим. Так как движок не создаётся,
    наличие DBAPI не требуется.

    Вызовы context.execute() в этом режиме выводят SQL в виде строки.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Конфигурирует контекст Alembic и запускает миграции.

    Args:
        connection: Активное соединение с БД.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Создаёт асинхронный движок SQLAlchemy, открывает соединение
    и выполняет миграции в контексте Alembic.

    Используется для онлайн-режима, когда требуется асинхронная
    работа с базой данных.
    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме с подключением к базе данных."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
