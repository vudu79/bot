import logging
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

from handlers import client, admin, other
from create_bot import TOKEN, bot, dp



API_TOKEN = 'BOT_TOKEN_HERE'

# webhook settings
# WEBHOOK_HOST = 'https://your.domain'
# WEBHOOK_PATH = '/path/to/api'
WEBHOOK_URL = " https://451a-185-17-131-112.eu.ngrok.io"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 5000

logging.basicConfig(level=logging.INFO)

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

dp.middleware.setup(LoggingMiddleware())


@dp.message_handler()
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(message.chat.id, message.text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_URL,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )




# import json
# import logging, os
# import multiprocessing
#
# import aiogram.types
#
# from handlers import client, admin, other
# from create_bot import TOKEN, bot, dp
# from aiogram.utils.executor import start_webhook
# from echo_server import run, HttpGetHandler, HTTPServer
#
# HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
#
# # webhook settings
# WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
# WEBHOOK_PATH = f'/webhook/{TOKEN}'
# WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
#
# # webserver settings
# WEBAPP_HOST = '0.0.0.0'
# WEBAPP_PORT = os.getenv('PORT', default=8000)
#
#
# async def on_startup(dispatcher):
#     await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
#
#
# async def on_shutdown(dispatcher):
#     await bot.delete_webhook()
#
#
# client.register_handlers_client(dp)
# admin.register_handlers_admin(dp)
# other.register_handlers_other(dp)
#
# if __name__ == '__main__':
#
#     logging.basicConfig(level=logging.INFO)

    #
    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     skip_updates=True,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT,
    # )

    # kwa1 = {
    #     "dispatcher": dp,
    #     "webhook_path": WEBHOOK_PATH,
    #     "skip_updates": True,
    #     "on_startup": on_startup,
    #     "on_shutdown": on_shutdown,
    #     "host": WEBAPP_HOST,
    #     "port": WEBAPP_PORT,
    # }
    #
    # kwa2 = {
    #     "server_class" : HTTPServer,
    #     "handler_class": HttpGetHandler,
    # }

    # p1 = multiprocessing.Process(target=start_webhook, kwargs=kwa1)
    # p2 = multiprocessing.Process(target=run, kwargs=kwa2)
    # p1.start()
    # p2.start()
