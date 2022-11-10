import json

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os


TOKEN=os.getenv("BOT_TOKEN")

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

with open('calendar.json', 'r', encoding='utf-8') as f:
    js = f.read()

calendar_dict = json.loads(js)