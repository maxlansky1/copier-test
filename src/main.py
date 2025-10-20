# src/main.py

import asyncio
import redis.asyncio as redis
from configs.settings import settings
from src.utils.logger import get_logger  # ✅ Импортируем логгер

# Создаём логгер для main.py
logger = get_logger(__name__)  # ✅ Создаём экземпляр логгера


async def main():
    logger.info("🚀 Запуск приложения...")  # ✅ Логируем через кастомный логгер

    redis_client = redis.from_url(
        settings.database.redis.redis_url,
        db=settings.database.redis.redis_db,
        decode_responses=settings.database.redis.decode_responses,
    )

    try:
        await redis_client.ping()
        logger.info("✅ Подключились к Redis")  # ✅ Логируем успех

        cache_key = "tutorial_key"
        cache_value = "Hello, Redis with Custom User!"

        await redis_client.set(cache_key, cache_value, ex=settings.database.redis.redis_ttl)
        retrieved_value = await redis_client.get(cache_key)
        logger.info(f"📦 Закешировали и получили: {retrieved_value}")  # ✅ Логируем результат

    except Exception as e:
        logger.error(f"❌ Ошибка при работе с Redis: {e}")  # ✅ Логируем ошибку
    finally:
        await redis_client.aclose()
        logger.info("🔒 Закрыли соединение с Redis")  # ✅ Логируем закрытие


if __name__ == "__main__":
    asyncio.run(main())