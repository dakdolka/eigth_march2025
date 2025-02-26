from sqlalchemy import text, insert, select, func, cast, Integer, and_, update
from data.database import async_engine, async_session_factory
# from db.models import metadata_obj
from sqlalchemy.orm import aliased
from data.database import Base
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from data import models
from bot.circles import exceptions as ex

from data.models import ModerationState


class Orm:
    @staticmethod
    async def add_circle(note_id, user_id):
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
            
    @staticmethod
    async def send_video(man_id):
        async with async_session_factory() as session:
            video_id = (
                await session.execute(
                    select(models.Message.video_note_id).where(and_(models.Message.sender_tg_id == man_id, models.Message.moderation_state == ModerationState.APPROVED.name))
                )
            ).scalars().first()
            
            woman_tg_id = (
                await session.execute(
                    select(models.Man.woman_aim).where(models.Man.tg_id == man_id)
                )
            )

            return video_id, woman_tg_id
        
    @staticmethod
    async def upd_woman_score(woman_id):
        async with async_session_factory() as session:
            await session.execute(update(models.Woman).where(models.Woman.tg_id == woman_id).values(circles_reached=models.Woman.circles_reached + 1))
            await session.commit()