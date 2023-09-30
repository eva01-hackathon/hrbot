from aiogram import executor, Dispatcher

from config import dp, global_executor
import bot


async def on_startup(_: Dispatcher):
    ...


async def on_shutdown(_: Dispatcher):
    global_executor.shutdown(wait=True)


if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
