from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)
