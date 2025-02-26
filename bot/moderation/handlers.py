from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, callback_data
from aiogram.types import Message, CallbackQuery, ContentType, VideoNote
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.moderation import keyboards as kb
from bot.moderation import crud 
from config import BOT, settings
from bot.circles import exceptions as ex


rt = Router()

class System(StatesGroup):
    cancel_changes = State()


# @rt.message(CommandStart())
# async def echo(message: Message):
#     await message.answer(text=f'thread id: {message.message_thread_id}')


# @rt.message(F.content_type == ContentType.VIDEO_NOTE)
# async def echo(message: Message):
    

#     await message.answer(text='Спасибо за кружочек! Мы отправили его на модерацию')
#     await BOT.send_video_note(
#         chat_id=settings.group_id, 
#         message_thread_id=settings.not_approved_thread_id, 
#         video_note=message.video_note.file_id, 
#         reply_markup=kb.approve_kb(
#             id=message.from_user.id
#         )
#     )


# Отправка кружков на модерацию
async def send_note_to_moderation(message: Message):
    await message.answer(text='Спасибо за кружочек! Мы отправили его на модерацию')
    await BOT.send_video_note(
        chat_id=settings.group_id, 
        message_thread_id=settings.not_approved_thread_id, 
        video_note=message.video_note.file_id, 
        reply_markup=kb.approve_kb(
            id=message.from_user.id
        )
    )
    


# Если подтверждено
@rt.callback_query(kb.Approve.filter(F.is_approved == True))
async def approve(callback: CallbackQuery, state: FSMContext, callback_data: kb.Approve):
    print(callback_data.id)
    print('!!!!!!!!!!!!!')
    video_note_id = await crud.get_note_id(callback_data.id)
    await callback.message.delete()
    await callback.answer()
    print(callback_data)

    # Отправка в отдельную группу для модеров
    await BOT.send_video_note(
        chat_id=settings.group_id, 
        message_thread_id=settings.approved_thread_id, 
        video_note=video_note_id,
        reply_markup=kb.reject_kb(
            id=callback_data.id
        )
    )

    # Отправка пользователю
    await BOT.send_message(
        chat_id=callback_data.id, 
        text='Поздравляем! Ваше сообщение было одобрено! Спасибо за участие <3'
    )

    await crud.approve(callback_data.id)


# Если отклонено
@rt.callback_query(kb.Approve.filter(F.is_approved == False))
async def reject(callback: CallbackQuery, state: FSMContext, callback_data: kb.Approve):
    await callback.answer()
    video_note_id = await crud.get_note_id(callback_data.id)
    await callback.message.delete()
    
    # Дополнительное сообщение (dop_message)
    message = await callback.message.answer(text='Введите комментарий к отклонению кружка ниже:\n\nНачните сообщение с двойного слеша\nПример:"// не подходит"')

    # Пересылка кружочка, чтобы не путаться
    note = await BOT.send_video_note(
        chat_id=settings.group_id, 
        message_thread_id=callback.message.message_thread_id, 
        video_note=video_note_id,
        reply_markup=kb.cancel_changes(
            id=callback_data.id,
            is_approved_earlier=callback.message.message_thread_id == settings.approved_thread_id,
            dop_message_id=message.message_id
        )
    )

    await state.set_state(System.cancel_changes)
    await state.update_data(
        video_note_message_id = note.message_id,
        dop_message_id = message.message_id,
        user_id = callback_data.id,
        is_approved_earlier = callback.message.message_thread_id == settings.approved_thread_id,
        video_note_id = video_note_id
    )


# Отказаться от отклонения
@rt.callback_query(kb.CancelChanges.filter())
async def cancel_changes(callback: CallbackQuery, state: FSMContext, callback_data: kb.CancelChanges):
    await state.clear()
    await callback.answer()

    # Возвращение подходящих клавиатур
    if callback_data.is_approved_earlier:
        await callback.message.edit_reply_markup(reply_markup=kb.reject_kb(id=callback_data.id))
    else:
        await callback.message.edit_reply_markup(reply_markup=kb.approve_kb(id=callback_data.id))

    # удаление дополнительного сообщения
    await BOT.delete_message(
        chat_id=settings.group_id,
        message_id=callback_data.dop_message_id
    )
    
    

# Добавление описания к отклонению
@rt.message(System.cancel_changes, Command('/'))
async def end_rejection(message: Message, state: FSMContext):
    video_note_message_id = await state.get_value('video_note_message_id')
    dop_message_id = await state.get_value('dop_message_id')
    user_id = await state.get_value('user_id')
    is_approved_earlier = await state.get_value('is_approved_earlier')
    video_note_id = await state.get_value('video_note_id')
    await state.clear()
    
    # Подбор текста
    if is_approved_earlier:
        text = 'Упс, похоже мы нашли проблему, извините, что не обнаружили ее сразу...'
    else:
        text = 'К сожалению, ваше сообщение не прошло модерацию.'


    await BOT.delete_message(
        chat_id=settings.group_id,
        message_id=dop_message_id
    )
    await BOT.delete_message(
        chat_id=settings.group_id,
        message_id=video_note_message_id
    )
    await BOT.send_message(
        chat_id=settings.group_id,
        message_thread_id=settings.rejected_thread_id,
        text=f'=================\n\nКружок ниже отклонен по причине:\n\n{message.text[2:]}'
    )
    await BOT.send_video_note(
        chat_id=settings.group_id,
        message_thread_id=settings.rejected_thread_id,
        video_note=video_note_id
    )
    await BOT.send_message(
        chat_id=user_id,
        text=f'{text} Вот причина:\n\n{message.text[2:]}\n\nПопробуйте еще раз!'
    )
    await message.delete()

    await crud.reject(user_id)