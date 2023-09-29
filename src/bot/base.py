from aiogram import types

from config import dp
from .message_rate import rate_buttons


async def reply(m: types.Message, text: str) -> types.Message:
    return await m.reply(text, reply_markup=rate_buttons)


@dp.message_handler(commands=["start", "help"])
async def send_start(m: types.Message):
    await m.answer(
        f"Привет, {m.from_user.first_name}! Здесь ты можешь задать любые рабочие вопросы, которые тебя интересуют 💌\n"
        f"Просто напиши любое сообщение и я постараюсь на него ответить 🤓"
    )
