"""
Модуль для создания асинхронного движка и сессии SQLAlchemy.

Этот модуль настраивает подключение к базе данных SQLite с использованием
асинхронного движка SQLAlchemy. Он предоставляет все необходимые компоненты
для работы с базой данных в асинхронном режиме:

- `engine` — асинхронный движок, который управляет подключением к базе данных.
  Он отвечает за создание соединений, настройку пула соединений, логирование
  SQL-запросов и другие параметры подключения.

- `async_session` — фабрика асинхронных сессий, которая создает сессии
  для выполнения запросов к базе данных.
"""

from functools import wraps

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from configs.settings import settings

# Формируем путь и URL для подключения к БД
db_url: str = settings.database.sqlite.database_url


# Асинхронный движок с настройками из конфига
engine = create_async_engine(
    url=db_url,  # URL подключения к базе данных
    echo=settings.database.sqlite.echo,  # Логирование SQL-запросов
    pool_pre_ping=settings.database.sqlite.pool_pre_ping,  # Проверка соединения перед использованием
    pool_size=settings.database.sqlite.pool_size,  # Размер пула соединений
    max_overflow=settings.database.sqlite.max_overflow,  # Максимальное количество дополнительных соединений
)


# Фабрика асинхронных сессий
async_session = async_sessionmaker(
    engine,  # Движок, из которого создаются соединения
    expire_on_commit=settings.database.sqlite.expire_on_commit,  # Если True — объекты устаревают после commit
    autoflush=settings.database.sqlite.autoflush,  # Если True — автоматически синхронизирует изменения с БД
)


def connection(func):
    """
    Декоратор для автоматического управления сессией.

    Оборачивает асинхронную функцию, автоматически создавая и закрывая
    сессию базы данных. В случае ошибки выполняет откат транзакции.

    Args:
        func: Асинхронная функция, которая принимает сессию в качестве аргумента.

    Returns:
        Результат выполнения оборачиваемой функции.

    Example:
        @connection
        async def get_users(session):
            result = await session.execute(select(User))
            return result.scalars().all()
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        """
        Внутренняя функция-обёртка, управляющая сессией.

        Создаёт асинхронную сессию, передаёт её в оборачиваемую функцию,
        обрабатывает исключения и гарантирует закрытие сессии.
        """
        async with async_session() as session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откат при ошибке
                raise e
            finally:
                await session.close()  # Закрытие сессии

    return wrapper
