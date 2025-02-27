from data.database import async_session_factory
from data import models
from sqlalchemy import insert, select, update, delete, and_, or_
from data.models import ModerationState
from bot.moderation import keyboards as kb



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
    
async def who_needs_circles():
    async with async_session_factory() as session:
        stmt = (
            select(models.Woman)
            .where(
                models.Woman.circles_reached == 0
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()
    
async def send_video_note(woman_id, user_id, video_note):
    async with async_session_factory() as session:
        stmt = (
            insert(models.Message).values(
                sender_tg_id=user_id,
                video_note_id=video_note,
                moderation_state=ModerationState.APPROVED,
                receiver_id=woman_id
            )
        )
        await session.execute(stmt)
        await session.flush()
        await session.execute(update(models.Woman).where(models.Woman.tg_id == woman_id).values(circles_reached=models.Woman.circles_reached + 1))
        await session.commit()