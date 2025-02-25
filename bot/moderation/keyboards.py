from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import callback_data
from aiogram.filters.callback_data import CallbackData
from typing import Optional



class Approve(CallbackData, prefix='approve'):
    id: int
    is_approved: bool

class CancelChanges(CallbackData, prefix='cancel_changes'):
    id: int
    is_approved_earlier: bool
    dop_message_id: int



def approve_kb(id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтвердить', callback_data=Approve(id=id, is_approved=True).pack()),
            InlineKeyboardButton(text='Отклонить', callback_data=Approve(id=id, is_approved=False).pack())
        ]
    ])


def reject_kb(id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Отклонить', callback_data=Approve(id=id, is_approved=False).pack())
        ]
    ])

def cancel_changes(id, is_approved_earlier, dop_message_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Отменить изменения', callback_data=CancelChanges(id=id, is_approved_earlier=is_approved_earlier, dop_message_id=dop_message_id).pack())
        ]
    ])