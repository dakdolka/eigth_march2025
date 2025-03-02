from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.circles.crud import Orm
from config import settings, BOT
from bot.circles import exceptions as ex
from bot.circles.crud import send_video_notes, send_extras
from bot.moderation.handlers import send_note_to_moderation, System
import data.models as models

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
    
@rt.message(Command('add_circles'), F.chat.id == settings.group_id)
async def add_circles(message: Message, state: FSMContext):
    await state.clear()
    extras = await Orm.who_needs_circles()
    if len(extras) == 0:
        await message.answer(text='Все кружки готовы!')
        return
    pers = extras.pop()
    await state.update_data(extras=extras)
    await message.answer(text=f'{pers.name_sur}\n{pers.description}')
    await state.update_data(woman_to_send=pers)
    await state.set_state(System.admin_circle)


@rt.message(System.admin_circle, F.video_note)
async def save_video_note(message: Message, state: FSMContext):
    video_id = message.video_note.file_id
    woman: models.Woman = await state.get_value('woman_to_send')
    await Orm.send_video_note(
        woman.tg_id,
        message.from_user.id,
        video_id
    )
    extras = (await state.get_data())['extras']
    if len(extras) > 0:
        pers = extras.pop()
        await state.update_data(extras=extras)
        await message.answer(text=f'{pers.name_sur}\n{pers.description}')
        await state.update_data(woman_to_send=pers)
        await state.set_state(System.admin_circle)
    else:
        await message.answer(text='Все кружки готовы!')
        
@rt.message(Command('stop'), F.chat.id == settings.group_id)
async def stop(message: Message, state: FSMContext):
    await state.clear()
    
@rt.message(Command('congratulate'), F.chat.id == settings.group_id)
async def congratulate(message: Message, state: FSMContext):
    await send_video_notes(BOT)
    await send_extras(BOT)
    
# @rt.message(Command('test_woman_sending'))
# async def check_my(message: Message, state: FSMContext):
#     await send_video_notes(BOT)