from aiogram import Bot
from sqlalchemy import text, insert, select, func, cast, Integer, and_, update
from data.database import async_engine, async_session_factory
# from db.models import metadata_obj
from sqlalchemy.orm import aliased
from data.database import Base
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from data import models
from bot.circles import exceptions as ex
from data.models import Message
from data.models import ModerationState

class Orm:
    @staticmethod
    async def add_circle(user_id, note_id):
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
            
    @staticmethod
    async def get_women_circles():
        async with async_session_factory() as session:
            query = select(Message).where(Message.moderation_state == ModerationState.APPROVED).options(selectinload(Message.man))
            result = await session.execute(query)
            return result.scalars().all()
        
    @staticmethod
    async def get_extra_circles():
        async with async_session_factory() as session:
            result = await session.execute(select(Message).where(Message.receiver_id != 0))
            return result.scalars().all()
    

async def send_video_notes(bot: Bot):
    for elem in await Orm.get_women_circles():
        try:
            await bot.send_video_note(chat_id=elem.man.woman_aim, video_note=elem.video_note_id)
        except:
            pass
        
async def send_extras(bot: Bot):
    for elem in await Orm.get_extra_circles():
        await bot.send_video_note(chat_id=elem.receiver_id, video_note=elem.video_note_id)