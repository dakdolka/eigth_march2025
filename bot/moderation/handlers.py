from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, callback_data
from aiogram.types import Message, CallbackQuery, ContentType, VideoNote
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.moderation import keyboards as kb
from config import BOT


rt = Router()


@rt.message(CommandStart())
async def echo(message: Message):
    await message.answer(text=str(message.chat.id) + ' ' + str(message.message_thread_id), reply_markup=None)


@rt.message(F.content_type == ContentType.VIDEO_NOTE)
async def echo(message: Message):
    print(1)
    await BOT.send_video_note(chat_id=-1002467822218, message_thread_id=5, video_note=message.video_note.file_id, reply_markup=kb.approve)