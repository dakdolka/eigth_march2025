from aiogram import Router
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, callback_data
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import bot.keyboards as kb

from data.orm import Orm

rt = Router()

class Women(StatesGroup):
    tg_id = State()
    description = State()

@rt.message(CommandStart())
async def echo(message):
    await message.answer(text='ваш пол', reply_markup=kb.start_kb)
    
@rt.callback_query(F.data == 'woman')
async def woman(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Women.description)
    await callback.message.edit_text(text='бамбам, ждём описание')
    
@rt.message(Women.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(tg_id= message.from_user.id, description=message.text)
    await message.answer(text='подтвердите', reply_markup=kb.approve_desc)
    
@rt.callback_query(F.data == 'approve_desc')
async def approve_desc(callback: CallbackQuery, state: FSMContext):
    print(await state.get_data())
    await Orm.insert_woman(await state.get_data())
    await callback.message.edit_text(text='Ждите поздравления!')
    

@rt.callback_query(F.data == 'man')
async def man(callback: CallbackQuery):
    await callback.message.edit_text(text='Ждите женщину!')