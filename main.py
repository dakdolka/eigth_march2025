from aiogram import Dispatcher
import asyncio
from config import settings, BOT
from bot.reg.handlers import rt as rt_reg
from bot.moderation.handlers import rt as rt_mod
from config import settings
from bot.reg.handlers import rt as reg_rt
from bot.circles.handlers import rt as circle_rt

from data.orm import Orm


dp = Dispatcher()

dp.include_router(rt_mod)
dp.include_router(rt_reg)
dp.include_router(reg_rt)
dp.include_router(circle_rt)

async def main():
    await Orm.create_all()
    await dp.start_polling(BOT)
    await Orm.add_woman_to_test()
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())

