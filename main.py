from aiogram import Dispatcher
import asyncio
from config import settings, BOT
# from bot.reg.handlers import rt
from bot.moderation.handlers import rt

from data.orm import Orm


dp = Dispatcher()
dp.include_router(rt)

async def main():
    await Orm.create_all()
    await dp.start_polling(BOT)
    
if __name__ == '__main__':
    asyncio.run(main())

