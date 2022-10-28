from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

asosiy = ReplyKeyboardMarkup(resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🛍 Buyurtma berish")],
        [KeyboardButton(text="📦 Buyurtmalarim"), KeyboardButton(text="ℹ️ Biz haqimizda")],
        # [KeyboardButton(text="Sozlamalar"), KeyboardButton(text="Fikr qoldirish")]

    ]
)