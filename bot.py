import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.handlers.start import register_start
from tgbot.handlers.weather import register_weather
from tgbot.handlers.converter import register_converter
from tgbot.handlers.random_cat_photo import register_cat_photo
from tgbot.handlers.creating_poll import register_creating_poll

logger = logging.getLogger(__name__)


def register_all_handlers(dp):
    register_start(dp)
    register_weather(dp)
    register_converter(dp)
    register_cat_photo(dp)
    register_creating_poll(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)

    bot["config"] = config
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
