from aiogram import executor

from config import dp
import bot


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
