from distutils.command.config import config
from loader import dp, db, bot 
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import LabeledPrice
from utils.misc.product import Product

@dp.callback_query_handler(text_contains="pay")
async def get_order_id(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    order_id = call.data.split(":")[-1]
    order = db.get_payment_order(tg_id=call.from_user.id, order_id=order_id)
    text = order[2].replace("<i>", "")
    text = text.replace("</i>", "")
    products = Product(
        title = "To'lov uchun tugmani bosing.",
        description=text,
        currency="UZS",
        prices=[
            LabeledPrice(
                label='Barcha buyurtmalar',
                amount=order[3] * 100,
        ),
        #     LabeledPrice(
        #         label='Yetkazib berish (7 kun)',
        #         amount=2000000,# 20 000.00 so'm
        # ),
        ],
        start_parameter="create_invoice_products",
        photo_url='https://play-lh.googleusercontent.com/8TUCh0tgZ8swZ96Q9t3IZJUGjeUjCBFODobu5oXAvUVVk4D-OvfW8sP9RhfkopE8FBE',
        photo_width=1280,
        photo_height=1100,
        # photo_size=600,
        need_email=True,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True, # foydalanuvchi manzilini kiritishi shart
        is_flexible=True,
        

    )

    await bot.send_invoice(chat_id=call.from_user.id, **products.generate_invoice(), payload="payload:products")
    await call.answer("To'lov qilishingiz mumkin")
    await state.update_data(
        {"pay_order_id": order_id}
    )