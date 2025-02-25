from data.database import async_session_factory
from data import models
from sqlalchemy import select


async def get_note_id(user_id):
    async with async_session_factory() as session:
        stmt = select(models.Man.circle).where(models.Man.tg_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()


async def insert_note(note_id, user_id):
    async with async_session_factory() as session:
        session.add(models.Man(circle=note_id, tg_id=user_id))
        await session.commit()