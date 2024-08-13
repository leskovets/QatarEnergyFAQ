import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage

from config import settings
from bot.routers import router as main_router


async def main() -> None:

    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger('main')
    logger.debug('Start main')

    storage = RedisStorage.from_url(settings.REDIS_URL)

    bot = Bot(settings.API_TOKEN_TELEGRAM)
    dp = Dispatcher(storage=storage)

    dp.include_router(main_router)

    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logger.error(ex)


if __name__ == '__main__':
    asyncio.run(main())
