from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


approve = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Подтвердить', callback_data='approve'), 
        InlineKeyboardButton(text='Отклонить', callback_data='edit_desc')
    ]
])