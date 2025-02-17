import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from config import load_config
from db import Database
from handlers import register_handlers
from services.subscriptions import check_subscriptions
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Загружаем конфиг
config = load_config()

# Создаём бота и диспетчер
default_properties = DefaultBotProperties(parse_mode='HTML')
bot = Bot(token=config["BOT_TOKEN"], default=default_properties)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    # Инициализация базы данных
    db = Database(config)

    await db.connect()
    await db.create_users_table()
    await db.create_tariffs_table()
    await db.create_subscriptions_table()
    await db.create_vpn_keys_table()

    logger.info("Запуск бота...")

    # Передаём bot в register_handlers
    register_handlers(dp, db, bot)

    asyncio.create_task(check_subscriptions(db, bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
