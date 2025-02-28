from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='М', callback_data='man'), InlineKeyboardButton(text='Ж', callback_data='woman')]
])

approve_desc = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data='approve_desc'), InlineKeyboardButton(text='Изменить', callback_data='edit_desc')]
])

change_or_wait = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data='edit_desc'), InlineKeyboardButton(text='Ждём!', callback_data='wait')]
])

approve_circling = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да, я запишу поздравление!', callback_data='approve_circling')],
    [ InlineKeyboardButton(text='Нет, я передумал(', callback_data='deny_circling')]
])

reject_rejecting_circling = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да, я не хочу записывать.', callback_data='final_reject_circling')],
    [InlineKeyboardButton(text='Нет, кружочку быть!', callback_data='comeback')]
])