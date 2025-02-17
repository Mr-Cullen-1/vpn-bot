import os
import random
import string
from aiogram.types import InputFile
from services.xray_api import add_user, remove_user
from loguru import logger

VPN_CONFIG_DIR = r"C:\Users\user\Desktop\vpn_bot\bot-logic\vpn\configs"
if not os.path.exists(VPN_CONFIG_DIR):
    os.makedirs(VPN_CONFIG_DIR)

def generate_client_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

async def generate_vpn_key_and_config(db, user_id, bot):
    client_name = generate_client_name()
    uuid = ''.join(random.choices(string.hexdigits, k=32))

    added = await add_user(uuid, email=f"user_{user_id}@vpn.com")
    if not added:
        await bot.send_message(user_id, "Ошибка при создании VPN-подключения.")
        return None

    async with db.pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO vpn_keys (user_id, key) VALUES ($1, $2)",
            user_id, uuid
        )

    config = f"vless://{uuid}@mytelegramvpn.ru:443?encryption=none&type=tcp"
    await bot.send_message(user_id, f"Ваш VPN доступ:\n\n<code>{config}</code>")

    return uuid
