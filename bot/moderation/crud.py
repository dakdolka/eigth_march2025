from data.database import async_session_factory
from data import models
from sqlalchemy import insert, select, update, and_
from data.models import ModerationState

async def get_note_id(user_id):
    async with async_session_factory() as session:
        stmt = (
            select(models.Message.video_note_id)
            .where(
                and_(
                    models.Message.sender_tg_id == user_id,
                    models.Message.moderation_state != ModerationState.REJECTED.name
                )
            )
        )
        result = await session.execute(stmt)
        return result.scalars().first()


async def approve(user_id):
    async with async_session_factory() as session:
        stmt = (
            update(models.Message)
            .where(and_(
                models.Message.sender_tg_id == user_id, 
                models.Message.moderation_state == ModerationState.PENDING.name
            ))
            .values(moderation_state=ModerationState.APPROVED)
        )
        await session.execute(stmt)
        await session.commit()


async def reject(user_id):
    async with async_session_factory() as session:
        stmt = (
            update(models.Message)
            .where(and_(
                models.Message.sender_tg_id == user_id, 
                models.Message.moderation_state != ModerationState.REJECTED.name
            ))
            .values(moderation_state = ModerationState.REJECTED)
            )
        await session.execute(stmt)
        await session.commit()