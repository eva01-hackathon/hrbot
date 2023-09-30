import asyncio
from threading import Thread
import time


from aiogram import types, Bot

from config import dp, bot, global_executor
from .base import reply
from llama_model import SYSTEM_PROMPT, generate


def run_coro(coro, loop: asyncio.AbstractEventLoop):
    fut = asyncio.run_coroutine_threadsafe(coro, loop)
    return fut.result()


def fake_process(
    message: types.Message,
    loop: asyncio.AbstractEventLoop,
    temp_msg: types.Message,
) -> str:
    Bot.set_current(bot)

    history = [[message.text, SYSTEM_PROMPT]]

    results = generate(history, SYSTEM_PROMPT, 0.9, 30, 0.01)
    for res in results:
        pass
    res = res[0][-1]
    run_coro(reply(message, res), loop)
    run_coro(temp_msg.delete(), loop)


@dp.message_handler()
async def dialog_handler(m: types.Message):
    loop = asyncio.get_running_loop()
    temp_msg = await m.reply("⌛️ Ожидайте...")
    await m.answer_chat_action(types.ChatActions.TYPING)
    args = (m, loop, temp_msg)
    global_executor.submit(fake_process, *args)
    # Thread(target=fake_process, args=args).start()
    ...
