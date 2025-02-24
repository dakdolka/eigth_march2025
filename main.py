from aiogram import Bot, Dispatcher
import asyncio
from config import settings
from bot.reg.handlers import rt

from data.orm import Orm

bot = Bot(token=settings.token)
dp = Dispatcher()
dp.include_router(rt)

async def main():
    await Orm.create_all()
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())

