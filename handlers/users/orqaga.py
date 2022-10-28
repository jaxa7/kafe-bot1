from loader import dp, db 
from aiogram import types
from keyboards.default.main_menu import asosiy
from states.holat import Kafe
from aiogram.dispatcher import FSMContext
from keyboards.default.cats import cats_keyboard



@dp.message_handler(text="Orqaga", state=Kafe.cats)
async def get_menu(message: types.Message, state: FSMContext):
    await message.answer("Siz asosiy menyuga qaytdingiz", reply_markup=asosiy)
    await state.finish()

@dp.message_handler(text="Orqaga", state=Kafe.sub_cat)
async def get_cat(message: types.Message):
    await message.answer("Kategoriyani tanlang", reply_markup=cats_keyboard)
    await Kafe.cats.set()

@dp.message_handler(text="Orqaga", state=Kafe.savat)
async def get_cat_back(message: types.Message):
    await message.answer("Kategoriyani tanlang", reply_markup=cats_keyboard)
    await Kafe.cats.set()

@dp.message_handler(text="Orqaga", state=Kafe.product)
async def get_cat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sub_cat_id =data["sub_cat_id"]
    cat_id = db.select_all_sub_back(id= sub_cat_id)[0]
    print(cat_id)
    sub_cats = db.select_all_sub_cat(cat_id=cat_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in sub_cats:
        markup.insert(types.KeyboardButton(text=i[0]))
    markup.add(types.KeyboardButton(text="Savatcha"), types.KeyboardButton(text="Orqaga"))
    await message.answer(f"Select subcategory", reply_markup=markup)
    await Kafe.next()
    await Kafe.sub_cat.set()


@dp.message_handler(text="Orqaga", state=Kafe.amount)
async def  get_product_back(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sub_cat_id =data["sub_cat_id"]
    products = db.select_all_products(sub_cat_id=sub_cat_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for product in products:
        markup.insert(types.KeyboardButton(text=str(product[0])))
    markup.add(types.KeyboardButton(text="Savatcha"), types.KeyboardButton(text="Orqaga"))
    await message.answer(f"Ro'yxatidagi mahsulotlar", reply_markup=markup)
    products = db.select_all_products(sub_cat_id=sub_cat_id)
    await Kafe.product.set()