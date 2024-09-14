import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from routers.general.router import router as general_router
from routers.conversation.router import router as conversation_router

from bot.src.config import settings

dp = Dispatcher()
dp.include_routers(general_router, conversation_router)


async def main() -> None:
    bot = Bot(token=settings.token)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
