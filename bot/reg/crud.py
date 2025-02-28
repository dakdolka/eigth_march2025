from sqlalchemy import select, func, update
from data.database import async_session_factory
from data.models import Man, Woman

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
            min_sircles = (await session.execute(select(func.min(Woman.circles_reached)))).scalars().first()
            woman: Woman = await session.execute(select(Woman).filter(Woman.circles_reached == min_sircles).order_by(Woman.reg_time))
            woman: Woman = woman.scalars().first()
            return woman
            