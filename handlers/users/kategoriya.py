from aiogram import types
from keyboards.default import cats, nums
from loader import dp, db
from states.holat import Kafe
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext

@dp.message_handler(text="🛍 Buyurtma berish")
async def bot_echo(message: types.Message):
    await message.answer("Nimadan boshlaymiz?", reply_markup=cats.cats_keyboard)
    await Kafe.cats.set()

@dp.message_handler(state=Kafe.cats)
async def get_sub_cats(message: types.Message):
    cat = message.text 
    sub_cat_id = db.select_sub_cat_id(name=cat)[0]
    sub_cats = db.select_all_sub_cat(cat_id=sub_cat_id)
    if len(sub_cats) == 0:
        await message.answer("Ma'lumot topilmadi")
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for i in sub_cats:
            markup.insert(KeyboardButton(text=i[0]))
        markup.add(KeyboardButton(text="Savatcha 🧰"), KeyboardButton(text="Orqaga"))
        await message.answer(f"Select subcategory", reply_markup=markup)
        await Kafe.next()

@dp.message_handler(state=Kafe.sub_cat)
async def get_all_prods(message: types.Message, state: FSMContext):
    sub_cat = message.text
    sub_cat_id = db.get_sub_cat_id(name=sub_cat)[0]
    products = db.select_all_products(sub_cat_id=sub_cat_id)
    await state.update_data(
        {"sub_cat_id": sub_cat_id}
    )
    if len(products) == 0:
        await message.answer("Mahsulot topilmadi")
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for product in products:
            markup.insert(KeyboardButton(text=str(product[0])))
        markup.add(KeyboardButton(text="Savatcha 🧰"), KeyboardButton(text="Orqaga"))
        await message.answer(f"{sub_cat} ro'yxatidagi mahsulotlar", reply_markup=markup)
        await Kafe.next()

@dp.message_handler(state=Kafe.product)
async def get_prod_data(message: types.Message, state: FSMContext):
    name = message.text
    data = db.get_prod_info(name=name)
    await state.update_data(
            {"product": name, "price": data[-2]}
        )
    
    msg = f"{data[1]}\nNarxi: {data[-2]} so'm\n\n{data[2]}"
    await message.answer_photo(photo=data[3], caption=msg, reply_markup=nums.digits)
    await Kafe.next()

@dp.message_handler(state=Kafe.amount)
async def get_amount_product(message: types.Message, state: FSMContext):
    amount = message.text
    data = await state.get_data()  
    if int(amount) > 0:
        await message.answer(f"{data['product']} dan {amount} ta savatchangizga qo'shildi", reply_markup=cats.cats_keyboard)
        product = db.check_product(tg_id=message.from_user.id, name=data['product'])
        if product:
            quantity = product[2]
            db.update_product_cart(tg_id=message.from_user.id, name=data['product'], amount=quantity+int(amount))
        else:
            db.add_product_cart(tg_id=message.from_user.id, product=data['product'], amount=amount, price=data['price'])
    await Kafe.cats.set()
        
