from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_markup(order_id):
    markup = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton(text=" ⬅️", callback_data="prev"),
        InlineKeyboardButton(text="💰", callback_data=f"pay:{order_id}"),
        InlineKeyboardButton(text="➡️", callback_data="next")]
    ])
    return markup
