from aiogram import Bot, Dispatcher
import asyncio
from config import settings
from bot.reg.handlers import rt as reg_rt
from bot.circles.handlers import rt as circle_rt

from data.orm import Orm

bot = Bot(token=settings.token)
dp = Dispatcher()
dp.include_router(reg_rt)
dp.include_router(circle_rt)

async def main():
    await Orm.create_all()
    await Orm.add_woman_to_test()
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())

