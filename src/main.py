# src/main.py

import asyncio

import redis.asyncio as redis

from configs.settings import settings


async def main():
    print("🚀 Запуск приложения...")

    # Подключаемся к Redis, используя настройки из Pydantic
    redis_client = redis.from_url(
        settings.database.redis.redis_url,  # URL из настроек
        db=settings.database.redis.redis_db,
        password=settings.database.redis.redis_password,
        decode_responses=settings.database.redis.decode_responses,  # удобно для строк
    )

    try:
        # Простая проверка подключения
        await redis_client.ping()
        print("✅ Подключились к Redis")

        # Пример: сохранить и получить значение
        cache_key = "tutorial_key"
        cache_value = "Hello, Redis with Auth!"

        await redis_client.set(
            cache_key, cache_value, ex=settings.database.redis.redis_ttl
        )
        retrieved_value = await redis_client.get(cache_key)
        print(f"📦 Закешировали и получили: {retrieved_value}")

    except Exception as e:
        print(f"❌ Ошибка при работе с Redis: {e}")
    finally:
        await redis_client.aclose()
        print("🔒 Закрыли соединение с Redis")


if __name__ == "__main__":
    asyncio.run(main())
