from sqlalchemy import text, insert, select, func, cast, Integer, and_, update
from data.database import async_engine, async_session_factory
# from db.models import metadata_obj
from sqlalchemy.orm import aliased
from data.database import Base
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from data.models import Man, Woman


class Orm:
    @staticmethod
    async def add_circle(man_id, file_id):
        async with async_session_factory() as session:
            await session.execute(update(Man).where(Man.tg_id == man_id).values(circle=file_id))
            await session.commit()
            
    @staticmethod
    async def send_video(man_id):
        async with async_session_factory() as session:
            video_id, woman_id = (await session.execute(select(Man.circle, Man.woman_aim).where(Man.tg_id == man_id))).scalars().first()
            return (video_id, woman_id)
        
    @staticmethod
    async def upd_woman_score(woman_id):
        async with async_session_factory() as session:
            await session.execute(update(Woman).where(Woman.tg_id == woman_id).values(circles_reached=Woman.circles_reached + 1))
            await session.commit()