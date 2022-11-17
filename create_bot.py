import json

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

# TOKEN = os.getenv("TOKEN")
TOKEN = "5788022696:AAG6Vw4Feolg4LPQybsU0iAUUaE_UqhwwtQ"

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

with open('calendar.json', 'r', encoding='utf-8') as f:
    js = f.read()

calendar_dict = json.loads(js)

with open('calendar_storage.json', 'r', encoding='utf-8') as f:
    js = f.read()

calendar_storage = json.loads(js)
