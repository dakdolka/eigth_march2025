from aiogram import Router
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, callback_data
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import bot.reg.keyboards as kb

from bot.reg.crud import Orm
from bot.circles.handlers import Man

rt = Router()

class Women(StatesGroup):
    tg_id = State()
    description = State()


@rt.message(CommandStart())
async def echo(message: Message):
    flag = await Orm.check_if_exsist(message.from_user.id)
    if not flag:
        await message.answer(text='Привет! Кто ты?)', reply_markup=kb.start_kb)
    elif flag == 'woman':
        await message.answer(text='Хотите дополнить описание, пока ждёте поздравление?', reply_markup=kb.change_or_wait)
    elif flag == 'man':
        await message.answer(text='Ждите женщину!') #TODO
    
@rt.callback_query(F.data == 'woman')
async def woman(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Women.description)
    await callback.message.edit_text(text='бамбам, ждём описание')
    
@rt.message(Women.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(tg_id= message.from_user.id, description=message.text)
    await state.set_state(None)
    await message.answer(text=f'Текущее: {(await state.get_data())["description"]}\n подтвердите', reply_markup=kb.approve_desc)
    
@rt.callback_query(F.data == 'edit_desc')
async def edit_desc(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Women.description)
    await callback.message.edit_text(text=f'Текущее: {(await state.get_data())['description']}\n ждём новое описание')
    
@rt.callback_query(F.data == 'approve_desc')
async def approve_desc(callback: CallbackQuery, state: FSMContext):
    print(await state.get_data())
    await callback.answer()
    await Orm.insert_or_upd_woman(await state.get_data())
    await callback.message.edit_text(text='Ждите поздравления!')
    
@rt.message(Command('change_desc'))
async def change_desc(message: Message, state: FSMContext):
    flag = await Orm.check_if_exsist(message.from_user.id)
    if flag == 'woman':
        await state.set_state(Women.description)
        await message.answer(text=f'Текущее: {(await state.get_data())["description"]}\n введите описание')
    elif flag == 'man':
        await message.answer(text='Какие мы любопытные! Эта кнопочка только для деовчек :)')
    else:
        await message.answer(text='Ваш пол', reply_markup=kb.start_kb)

@rt.callback_query(F.data == 'man')
async def man(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    woman = await Orm.suggest_woman()
    await callback.message.edit_text(text=f'Ваша женщина: {woman.tg_id} Ждём кружок')
    await state.set_state(Man.circle)
    await Orm.insert_man({'tg_id': callback.from_user.id, 'woman_aim': woman.tg_id})