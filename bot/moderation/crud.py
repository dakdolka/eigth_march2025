from data.database import async_session_factory
from data import models
from sqlalchemy import select, update, delete, and_, or_
from data.models import ModerationState
from bot.moderation import exceptions as ex


async def insert_note(note_id, user_id):
    async with async_session_factory() as session:
        check_stmt = select(models.Message).where(
            and_(
                models.Message.sender_tg_id == user_id,
                models.Message.moderation_state != ModerationState.REJECTED.name
            )
        )
        result = await session.execute(check_stmt)
        if result.scalars().first():
            raise ex.MessageAlreadyExists

        session.add(models.Message(sender_tg_id=user_id, video_note_id=note_id))
        await session.commit()


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