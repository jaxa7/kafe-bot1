from datetime import datetime
from loader import dp, db 
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.cats import cats_keyboard
from states.holat import Kafe
from keyboards.default.nums import contact, location
from keyboards.default.main_menu import asosiy



@dp.message_handler(text="Savatcha 🧰", state="*")
async def get_card(message: types.Message, state: FSMContext): 
    # await state.finish()
    products = db.get_cart_products(tg_id=message.from_user.id)
    if len(products) > 0:
        total = 0
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        msg = f"<b>Sizning buyurtmalaringiz:</b>\n\n"
        for product in products:
            price = int(product[2]) * int(product[3])
            total += price
            msg += f"{product[1]} x {product[2]} = {price} so'm\n"
            markup.add(KeyboardButton(text=f"❌ {product[1]} ❌"))
        msg += f"\nJami: {total} so'm"
        markup.add(KeyboardButton(text="🛒 Buyurtma Berish"))
        markup.row(KeyboardButton(text="🗑 Bo'shatish"), KeyboardButton(text="Orqaga"))
        await message.answer(msg, reply_markup=markup)
        await Kafe.savat.set()
    else:
        await message.answer("Savatingiz bo'sh, buni tog'irlashni imkoni bor")


@dp.message_handler(state=Kafe.savat, text="🗑 Bo'shatish")
async def clean_cart(message: types.Message):
    db.clean_cart(tg_id=message.from_user.id)
    await message.answer("Savatingiz bo'shatildi", reply_markup=cats_keyboard)
    await Kafe.cats.set()

@dp.message_handler(state=Kafe.savat, text="🛒 Buyurtma Berish")
async def make_order(message: types.Message):
    await message.answer("Iltimos raqamingizni tasdiqlash", reply_markup=contact)
    await Kafe.phone.set()

@dp.message_handler(state=Kafe.phone, content_types=['contact'])
async def get_phone(message: types.Message, state: FSMContext):
    phone_num = message.contact.phone_number
    await state.update_data(
        {'phone': phone_num}
    )
    await message.answer("hozirgi joylashuvingizni jo'nating", reply_markup=location)
    await Kafe.location.set()

@dp.message_handler(state=Kafe.location, content_types=['location'])
async def get_location(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    data = await state.get_data()
    products = db.get_cart_products(tg_id=message.from_user.id)
    msg = ""
    total = 0
    for product in products:
        price = int(product[2]) * int(product[3])
        total += price
        msg += f"{product[1]} x {product[2]} = {price} so'm\n"
    phone = data.get('phone')
    await message.answer(f"Buyurtmangiz qo'shildi, siz bilan tezda bog'lanamiz!", reply_markup=asosiy)
    db.add_order(tg_id=message.from_user.id, product=msg, total_price=total, phone=phone, lat=lat, lon=lon, create=datetime.now())
    db.clean_cart(tg_id=message.from_user.id)
    await state.finish()

@dp.message_handler(state=Kafe.savat)
async def delete_product_cart(message: types.Message, state=FSMContext):
    name = message.text.replace("❌", "")
    product = name.strip()
    db.delete_product_cart(tg_id=message.from_user.id, name=product) #deleted
    total = 0
    products = db.get_cart_products(tg_id=message.from_user.id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    msg = f"<b>Sizning buyurtmalaringiz:</b>\n\n"
    for product in products:
        price = int(product[2]) * int(product[3])
        total += price
        msg += f"{product[1]} x {product[2]} = {price} so'm\n"
        markup.add(KeyboardButton(text=f"❌ {product[1]} ❌"))
    msg += f"\nJami: {total} so'm"

    await state.update_data(
        {'products': msg, 'total': total}
    )

    markup.add(KeyboardButton(text="🛒 Buyurtma Berish"))
    markup.row(KeyboardButton(text="🗑 Bo'shatish"), KeyboardButton(text="Orqaga"))
    await message.answer(msg, reply_markup=markup)
    await Kafe.savat.set()