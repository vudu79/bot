from aiogram import types, Dispatcher
import json, string
from main import dp


@dp.message_handler()
async def mat_filter_handler(message : types.Message):
    if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.text.split(' ')}\
            .intersection(set(json.load(open('json_mat.json')))) != set():

        await message.reply("Маты запрещены в чате")
        await message.delete()

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(mat_filter_handler)
