from loader import dp, db 
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.next_prev import create_markup

@dp.message_handler(text="📦 Buyurtmalarim")
async def get_my_orders(message: types.Message, state: FSMContext):
    order = db.get_order(tg_id=message.from_user.id)
    if order: 
        await state.update_data(
            {'order_id': order[0]}
        )
        await message.answer(text=f"Buyurtma raqami: №{order[0]}\n\n" + order[2] + f"\n<b>Umumiy: {order[3]}</b>", reply_markup=create_markup(order_id=order[0]))
    
    else:
        await message.answer("❌ Siz hech nima buyurmagansiz.")




@dp.callback_query_handler(text="next")
async def get_next_order(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    order_id = data.get('order_id')
    
    next = db.get_next_order(tg_id=call.from_user.id, order_id=order_id) 
    if next:
        await call.message.edit_text(text=f"Buyurtma raqami: №{next[0]}\n\n" + next[2] + f"\n<b>Umumiy: {next[3]}</b>", reply_markup=create_markup(order_id=next[0])) 
        
        await state.update_data(
            {'order_id': next[0]}
        )
    
    else:
        await call.answer("✅ Bu oxirgi buyurtmangiz.Boshqa buyurtma yo'q", show_alert=True)

@dp.callback_query_handler(text="prev")
async def get_prev_order(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    order_id = data.get('order_id')
    prevs = db.get_prev_order(tg_id=call.from_user.id, order_id=order_id) 
    if prevs:
        prev = prevs[-1]
        await call.message.edit_text(text=f"Buyurtma raqami: №{prev[0]}\n\n" + prev[2] + f"\n<b>Umumiy: {prev[3]}</b>", reply_markup=create_markup(order_id=prev[0])) 
        
        await state.update_data(
            {'order_id': prev[0]}
        )
    
    else:
        await call.answer("✅ Bu birinchi buyurtmangiz", show_alert=True)

@dp.message_handler(text="ℹ️ Biz haqimizda")
async def get_about(message: types.Message):
    await message.answer_photo(photo="https://www.nicepng.com/png/detail/115-1153072_go-to-image-julia-cafe-logo.png", caption="Семейное кафе Руккола.\n\nРежим работы: Пн-Сб, 10:00 - 21:00 \n\nЖалобы и предложения: @Jumaniyazov_5 , +998 90 558 26 46\n\n@myyfirstdemo_bot\n\nДоставка осуществляется по городу Хиве")
  