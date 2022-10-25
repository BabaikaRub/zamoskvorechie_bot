from aiogram.utils import executor

from create_bot import dp
from handlers import client
from db import connect_to_db, disconnect_from_db


async def on_startup(_):
    connect_to_db()
    print('[INFO] Bot is online')

client.registration_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    disconnect_from_db()
