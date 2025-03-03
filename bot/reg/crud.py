from sqlalchemy import delete, insert, select, func, update
from data.database import async_session_factory
from data.models import Man, Woman, Service

from config import BOT as bot
import bot.reg.keyboards as kb

import random


async def remind():
    for elem in await Orm.who_needs_remind():
        await bot.send_message(chat_id=elem.man_id, text='Время пришло! Нажмите накнопку ниже, и мы выдадим вашу цель :)', reply_markup=kb.extra_kb)
    await Orm.kill_service()
        

class Orm:
    @staticmethod
    async def insert_or_upd_woman(woman):
        async with async_session_factory() as session:
            if await Orm.check_if_exsist(woman['tg_id']) == 'woman':
                await session.execute(update(Woman).where(Woman.tg_id == woman['tg_id']).values(**woman))
                await session.commit()
                return
            session.add(Woman(**woman))
            await session.commit()
        async with async_session_factory() as session:
            service = (await session.execute(select(Service))).scalars().all()
            if service is not None:
                women = (await session.execute(select(Woman))).scalars().all()
                if len(women) > 8: #TODO изменить
                    await remind()
                    await session.commit()
                    
    @staticmethod
    async def upd_possible_circles(woman_id):
        async with async_session_factory() as session:
            await session.execute(update(Woman).where(Woman.tg_id == woman_id).values(circles_possible=Woman.circles_possible + 1))
            await session.commit()
            
            
            
    @staticmethod
    async def insert_man(man):
        async with async_session_factory() as session:
            session.add(Man(**man))
            await session.commit()
            
    @staticmethod
    async def check_if_exsist(tg_id):
        async with async_session_factory() as session:
            woman = await session.execute(select(Woman).where(Woman.tg_id == tg_id))
            woman = woman.scalars().first()
            if woman:
                return 'woman'
            man = await session.execute(select(Man).where(Man.tg_id == tg_id))
            man = man.scalars().first()
            if man:
                return 'man'
    @staticmethod
    async def suggest_woman():
        async with async_session_factory() as session:
            min_sircles = (await session.execute(select(func.min(Woman.circles_possible)))).scalars().first()
            women = await session.execute(select(Woman).filter(Woman.circles_possible == min_sircles).order_by(Woman.reg_time))
            women = women.scalars().all()
            woman = random.choice(women)
            return woman
        
    @staticmethod
    async def who_needs_remind():
        async with async_session_factory() as session:
            stmt = (
                select(Service)
            )
            res = await session.execute(stmt)
            res = res.scalars().all()
            return res
        
    @staticmethod
    async def kill_service():
        async with async_session_factory() as session:
            await session.execute(delete(Service))
            await session.commit()
            
    @staticmethod
    async def check_is_open():
        async with async_session_factory() as session:
            stmt = (
                select(Woman)
            )
            res = await session.execute(stmt)
            res = res.scalars().all()
            print(res)
            if len(res) > 8: #TODO изменить
                return True
            return False
    
    @staticmethod
    async def set_remind(id):
        async with async_session_factory() as session:
            stmt = (
                insert(Service).values(man_id=id)
            )
            await session.execute(stmt)
            await session.commit()
            