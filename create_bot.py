from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
import os


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
