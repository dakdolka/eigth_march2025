from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import callback_data
from aiogram.filters.callback_data import CallbackData

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='М', callback_data='man'), InlineKeyboardButton(text='Ж', callback_data='woman')]
])

approve_desc = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data='approve_desc'), InlineKeyboardButton(text='Изменить', callback_data='edit_desc')]
])

change_or_wait = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data='edit_desc'), InlineKeyboardButton(text='Ждём!', callback_data='wait')]
])
