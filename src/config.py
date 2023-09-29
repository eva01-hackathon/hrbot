import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TG_TOKEN")
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_HOST = os.getenv("MONGO_HOST")

MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
DB_NAME = "hrbot"

bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MongoStorage(uri=MONGO_URL, db_name=DB_NAME))
logger = logging.getLogger("bot")
