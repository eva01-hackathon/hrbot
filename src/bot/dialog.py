import asyncio
from threading import Thread


from aiogram import types, Bot

from config import dp, bot, global_executor
from .base import reply
from llama_model import SYSTEM_PROMPT, generate


def run_coro(coro, loop: asyncio.AbstractEventLoop):
    fut = asyncio.run_coroutine_threadsafe(coro, loop)
    return fut.result()


def fake_process(message: types.Message, loop: asyncio.AbstractEventLoop, history: list[list[str]]) -> str:
    Bot.set_current(bot)

    history = history if history else [[message.text, SYSTEM_PROMPT]]

    results = generate(history, SYSTEM_PROMPT, 0.9, 30, 0.01)
    answers = list(results)
    res = answers[0][0][-1]
    coro = reply(message, res)
    return run_coro(coro, loop)


@dp.message_handler()
async def dialog_handler(m: types.Message):
    loop = asyncio.get_running_loop()
    await m.answer_chat_action(types.ChatActions.TYPING)
    # global_executor.submit(fake_process, m, loop)
    Thread(target=fake_process, args=(m, loop, [])).start()
