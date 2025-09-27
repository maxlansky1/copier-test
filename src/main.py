"""
Точка входа — интерактивный CRUD-интерфейс с SQLite.

Этот модуль позволяет:
- Создавать, читать, обновлять и удалять пользователей
- Использовать Faker для генерации тестовых данных
- Логировать действия через кастомный логгер
"""

import asyncio
from faker import Faker
from sqlalchemy import select, delete
from src.databases.sqlite.core import async_session, engine, Base  # ✅ Импортируем Base отсюда
from src.databases.sqlite.models.user import User
from src.utils.logger import get_logger

# Получаем логгер
logger = get_logger(__name__)
faker = Faker()


async def create_user(count: int = 1):
    """
    Создаёт случайных пользователей с помощью Faker.

    Args:
        count (int): количество пользователей для создания
    """
    async with async_session() as session:
        for _ in range(count):
            new_user = User(
                username=faker.user_name(),
                email=faker.email(),
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            logger.info(f"Создан пользователь: {new_user}")

        logger.info(f"Создано {count} пользователей.")


async def read_users():
    """
    Читает всех пользователей из БД.
    """
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

        if not users:
            logger.info("БД пуста.")
            return

        for user in users:
            logger.info(f"Найден пользователь: {user}")


async def update_user():
    """
    Обновляет пользователя по ID (ввод с клавиатуры).
    """
    user_id = int(input("Введите ID пользователя для обновления: "))
    new_username = input("Введите новое имя (оставьте пустым, если не меняется): ").strip() or None
    new_email = input("Введите новый email (оставьте пустым, если не меняется): ").strip() or None

    if not new_username and not new_email:
        logger.warning("Нет данных для обновления.")
        return

    async with async_session() as session:
        user = await session.get(User, user_id)
        if not user:
            logger.warning(f"Пользователь с ID {user_id} не найден.")
            return

        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email

        await session.commit()
        logger.info(f"Обновлён пользователь: {user}")


async def delete_user():
    """
    Удаляет пользователя по ID (ввод с клавиатуры).
    """
    user_id = int(input("Введите ID пользователя для удаления: "))

    async with async_session() as session:
        user = await session.get(User, user_id)
        if not user:
            logger.warning(f"Пользователь с ID {user_id} не найден.")
            return

        await session.delete(user)
        await session.commit()
        logger.info(f"Удалён пользователь: {user}")


def show_menu():
    """Показывает меню."""
    print("\n" + "=" * 40)
    print("Выберите действие:")
    print("1. Создать пользователя(-ей)")
    print("2. Просмотреть всех пользователей")
    print("3. Обновить пользователя")
    print("4. Удалить пользователя")
    print("0. Выйти")
    print("=" * 40)


async def main():
    # Создаём таблицы при запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    while True:
        show_menu()
        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            count_input = input("Сколько пользователей создать? (по умолчанию 1): ").strip()
            count = int(count_input) if count_input.isdigit() else 1
            await create_user(count)
        elif choice == "2":
            await read_users()
        elif choice == "3":
            await update_user()
        elif choice == "4":
            await delete_user()
        elif choice == "0":
            logger.info("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    print("Программа завершена.")


if __name__ == "__main__":
    asyncio.run(main())