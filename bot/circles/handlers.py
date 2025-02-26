from aiogram import Router
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, callback_data
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.circles.crud import Orm
from aiogram.filters.state import StateFilter
from config import settings, BOT
from bot.circles import exceptions as ex
from bot.moderation.handlers import send_note_to_moderation
rt = Router()


class Man(StatesGroup):
    circle = State()

@rt.message(Man.circle, F.video_note)
async def save_video_note(message: Message, state: FSMContext):
    video_id = message.video_note.file_id
    try:
        await Orm.add_circle(message.from_user.id, video_id)
    except ex.MessageAlreadyExists:
        await message.answer(text='Кружочек уже был отправлен')
        return
    
    await send_note_to_moderation(message)
    
    
    
@rt.message(Command('test_woman_sending'))
async def check_my(message: Message, state: FSMContext):
    info = await Orm.send_video(message.from_user.id)
    await BOT.send_video_note(chat_id=info[1], video_note=info[0])
    await message.answer(text='кружок отправлен')
    await Orm.upd_woman_score(info[1])