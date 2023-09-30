import asyncio
import random
import time
from functools import partial
from concurrent.futures import as_completed
from threading import Thread

from aiogram import types, Bot

from config import dp, bot, global_executor
from .base import reply


def run_coro(coro, loop: asyncio.AbstractEventLoop):
    fut = asyncio.run_coroutine_threadsafe(coro, loop)
    return fut.result()


def fake_process(message: types.Message, loop: asyncio.AbstractEventLoop) -> str:
    Bot.set_current(bot)
    run_coro(message.answer_chat_action(types.ChatActions.TYPING), loop)
    # some processing here
    time.sleep(5)
    answer = random.choice(["Да", "Нет", "Не знаю"])
    coro = reply(message, answer)
    run_coro(coro, loop)


@dp.message_handler()
async def dialog_handler(m: types.Message):
    loop = asyncio.get_running_loop()
    # fake_process(m, loop)
    # Thread(target=fake_process, args=(m, loop)).start()
    future = global_executor.submit(fake_process, m, loop)
    # time.sleep(6)
    # completed = list(as_completed([future]))
    # print(completed)
    # [print(f.result()) for f in completed]