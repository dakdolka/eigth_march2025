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
    name = State()
    surname = State()
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
    await callback.message.edit_text(text='Для начала, расскажите что-нибудь о себе)')
    
@rt.message(Women.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(tg_id=message.from_user.id, description=message.text, name=message.from_user.first_name, surname=message.from_user.last_name)
    await state.set_state(None)
    await message.answer(text=f'Текущее описание: {(await state.get_data())["description"]}\n Для продолжения подтвердите, что всё корректно :)', reply_markup=kb.approve_desc)
    
@rt.callback_query(F.data == 'edit_desc')
async def edit_desc(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Women.description)
    await callback.message.edit_text(text=f'Текущее описание: {(await state.get_data())['description']}\n Отправьте изменённое описание. Вы также можете изменить описание по команде /change_desc')
    
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
        await message.answer(text='Привет! Кто ты?)', reply_markup=kb.start_kb)

@rt.callback_query(F.data == 'man')
async def man(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    woman = await Orm.suggest_woman()
    await state.update_data(woman=woman)
    await callback.message.edit_text(text=f'Ваша цель: {woman.name} {woman.surname}\nОписание:\n{woman.description}', reply_markup=kb.approve_circling)
    await Orm.insert_man({'tg_id': callback.from_user.id, 'woman_aim': woman.tg_id})
    

@rt.callback_query(F.data == 'approve_circling')
async def approve_circling(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    woman = (await state.get_data())['woman']
    await state.set_state(Man.circle)
    await callback.message.edit_text(text=f'Ваша цель: {woman.name} {woman.surname}\nОписание:\n{woman.description}\n\nОтлично, будем ждать вашего поздравления, когда будете готовы - просто отправляйте кружок в этот чат. Если от бота не последует реакции - пишите сюда @dak_dolka' )
    
    
@rt.callback_query(F.data == 'deny_circling')
async def reject_circling(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=f'Вы отказались записывать поздравление. Вы уверены, что хотите оставить девочку без поздравления в такой отличный праздник? Отказавшись от записи вы не сможете вернуться(', reply_markup=kb.reject_rejecting_circling)

@rt.callback_query(F.data == 'final_reject_circling')
async def final_reject_circling(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='Окей. Хорошего дня!)') #TODO проверить, что ничего не нужно в бд вносить
    
    
@rt.callback_query(F.data == 'comeback')
async def reject_rejecting_circling(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    woman = (await state.get_data())['woman']
    await callback.message.edit_text(text=f'Правльное решение :)\nВаша цель: {woman.name} {woman.surname}\nОписание:\n{woman.description}\nКогда будете готовы - просто отправляйте кружок в этот чат. Если от бота не последует реакции - пишите сюда @dak_dolka')
    

    