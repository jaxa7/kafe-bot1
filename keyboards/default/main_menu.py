from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

asosiy = ReplyKeyboardMarkup(resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="đ Buyurtma berish")],
        [KeyboardButton(text="đĻ Buyurtmalarim"), KeyboardButton(text="âšī¸ Biz haqimizda")],
        # [KeyboardButton(text="Sozlamalar"), KeyboardButton(text="Fikr qoldirish")]

    ]
)