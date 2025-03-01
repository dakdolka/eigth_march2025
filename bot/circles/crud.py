from aiogram import Bot
from sqlalchemy import insert, select, and_, update
from data.database import async_session_factory
from sqlalchemy.orm import selectinload
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
    async def upd_woman_score(man_id):
        async with async_session_factory() as session:
            man: models.Man = (await session.execute(select(models.Man).where(models.Man.tg_id == man_id).options(selectinload(models.Man.aim)))).scalars().first()
            await session.execute(update(models.Woman).where(models.Woman.tg_id == man.aim.tg_id).values(circles_reached=int(man.aim.circles_reached) + 1))
            await session.commit()
            
    @staticmethod
    async def get_women_circles():
        async with async_session_factory() as session:
            query = select(Message).where(and_(Message.moderation_state == ModerationState.APPROVED, Message.receiver_id == 0)).options(selectinload(Message.man))
            result = await session.execute(query)
            return result.scalars().all()
        
    @staticmethod
    async def get_extra_circles():
        async with async_session_factory() as session:
            result = await session.execute(select(Message).where(Message.receiver_id != 0))
            return result.scalars().all()
        
    @staticmethod
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
    
    @staticmethod
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
    

async def send_video_notes(bot: Bot):
    for elem in await Orm.get_women_circles():
        try:
            # print('uuuu\n', elem, 'uuuuu\n')
            await bot.send_video_note(chat_id=elem.man.woman_aim, video_note=elem.video_note_id)
            # print('ss')
        except:
            pass
        
async def send_extras(bot: Bot):
    for elem in await Orm.get_extra_circles():
        # print('uuuuuuuuuuuuuuuuuuuuuuu\n\n', elem, 'uuuuuuuuuuuuuuuuuu\n\n')
        await bot.send_video_note(chat_id=elem.receiver_id, video_note=elem.video_note_id)
        

