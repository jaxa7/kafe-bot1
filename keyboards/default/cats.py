from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db

kategoriya = db.select_all_categories()

print(kategoriya)

cats_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

for k in kategoriya:
    cats_keyboard.insert(KeyboardButton(text=k[1]))
cats_keyboard.add(KeyboardButton(text="Savatcha 🧰"), KeyboardButton(text="Orqaga"))