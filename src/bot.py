from aiogram import types

from config import dp


@dp.message_handler(commands=["start"])
async def send_start(m: types.Message):
    await m.answer(f"Hello, {m.from_user.first_name}!")
