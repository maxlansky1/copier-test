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
from src.databases.sqlite.core import async_session, engine, Base
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
        created = 0
        attempts = 0
        max_attempts = count * 5

        usernames = set()
        emails = set()
        users_to_add = []

        while created < count and attempts < max_attempts:
            username = faker.user_name()
            email = faker.email()

            if username in usernames or email in emails:
                attempts += 1
                continue

            usernames.add(username)
            emails.add(email)
            users_to_add.append({"username": username, "email": email})
            created += 1
            attempts += 1

        # Вставляем всё за раз
        if users_to_add:
            from sqlalchemy.dialects.sqlite import insert
            stmt = insert(User).values(users_to_add)
            await session.execute(stmt)
            await session.commit()
            logger.info(f"Создано {len(users_to_add)} пользователей.")

        if created < count:
            logger.warning(f"Не удалось создать {count - created} пользователей из-за ограничений уникальности.")


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
            # Проверяем уникальность
            result = await session.execute(
                select(User).where(User.username == new_username).where(User.id != user_id)
            )
            existing = result.scalars().first()
            if existing:
                logger.error(f"Пользователь с username '{new_username}' уже существует.")
                return

            user.username = new_username

        if new_email:
            # Проверяем уникальность
            result = await session.execute(
                select(User).where(User.email == new_email).where(User.id != user_id)
            )
            existing = result.scalars().first()
            if existing:
                logger.error(f"Пользователь с email '{new_email}' уже существует.")
                return

            user.email = new_email

        await session.commit()
        logger.info(f"Обновлён пользователь: {user}")


async def delete_user():
    """
    Удаляет пользователя по ID (ввод с клавиатуры).
    """
    choice = input("Удалить одного (1), несколько (2) или всех (3)? Введите 1/2/3: ").strip()

    async with async_session() as session:
        if choice == "1":
            user_id = int(input("Введите ID пользователя для удаления: "))
            user = await session.get(User, user_id)
            if not user:
                logger.warning(f"Пользователь с ID {user_id} не найден.")
                return

            await session.delete(user)
            await session.commit()
            logger.info(f"Удалён пользователь: {user}")

        elif choice == "2":
            ids_input = input("Введите ID пользователей через запятую (например: 1,2,3): ").strip()
            try:
                user_ids = [int(x.strip()) for x in ids_input.split(",")]
            except ValueError:
                logger.error("Неверный формат ID.")
                return

            result = await session.execute(delete(User).where(User.id.in_(user_ids)))
            await session.commit()

            deleted_count = result.rowcount
            logger.info(f"Удалено {deleted_count} пользователей.")

        elif choice == "3":
            confirm = input("Вы уверены, что хотите удалить всех пользователей? (y/N): ").strip().lower()
            if confirm == "y":
                result = await session.execute(delete(User))
                await session.commit()
                deleted_count = result.rowcount
                logger.info(f"Удалено {deleted_count} пользователей.")
            else:
                logger.info("Удаление отменено.")

        else:
            logger.warning("Неверный выбор.")


def show_menu():
    """Показывает меню."""
    print("\n" + "=" * 40)
    print("Выберите действие:")
    print("1. Создать пользователя(-ей)")
    print("2. Просмотреть всех пользователей")
    print("3. Обновить пользователя")
    print("4. Удалить пользователя (одного/нескольких/всех)")
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