from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, callback_data
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.moderation import keyboards as kb


rt = Router()


@rt.message(CommandStart())
async def echo(message: Message):
    await message.answer(text=message.chat.id, reply_markup=None)