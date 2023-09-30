import os
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorClient
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

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo_client.get_io_loop = asyncio.get_running_loop
db: Collection = mongo_client[DB_NAME]
ratings_db = db["rating"]

global_executor = ThreadPoolExecutor(max_workers=1)
