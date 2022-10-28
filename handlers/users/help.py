from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher import FSMContext
from loader import dp
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message, state: FSMContext):             
    await state.finish()
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")
    
    await message.answer("\n".join(text), reply_markup=ReplyKeyboardRemove())
