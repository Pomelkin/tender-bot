import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from general.router import router

from bot.src.config import settings

dp = Dispatcher()
dp.include_routers(router, )


async def main() -> None:
    bot = Bot(token=settings.token)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
