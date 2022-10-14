from aiogram.utils import executor
from handlers import client, admin, other
from create_bot import dp


async def on_startup(_):
    print("Бот вышел в онлайн")

client.register_handlers_client(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


