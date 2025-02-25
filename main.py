from aiogram import Dispatcher
import asyncio
from config import settings, BOT
from bot.reg.handlers import rt as rt_reg
from bot.moderation.handlers import rt as rt_mod

from data.orm import Orm


dp = Dispatcher()

dp.include_router(rt_mod)
dp.include_router(rt_reg)

async def main():
    await Orm.create_all()
    await dp.start_polling(BOT)
    
if __name__ == '__main__':
    asyncio.run(main())

