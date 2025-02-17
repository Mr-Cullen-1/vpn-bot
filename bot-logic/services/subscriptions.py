from datetime import datetime, timedelta
from loguru import logger
import asyncio
from services.xray_api import remove_user

async def deactivate_vpn(db, user_id):
    """Отключает пользователя от VPN и удаляет из Xray."""
    async with db.pool.acquire() as conn:
        key_data = await conn.fetchrow("SELECT key FROM vpn_keys WHERE user_id = $1", user_id)
        if key_data:
            uuid = key_data["key"]
            removed = await remove_user(uuid)
            if removed:
                await conn.execute("DELETE FROM vpn_keys WHERE user_id = $1", user_id)
                logger.info(f"VPN доступ для пользователя {user_id} был деактивирован.")
            else:
                logger.error(f"Ошибка при удалении пользователя {user_id} из Xray.")
        else:
            logger.warning(f"Попытка отключить несуществующий VPN-ключ для пользователя {user_id}")

async def check_subscriptions(db, bot):
    """Проверяет подписки и отключает пользователей с истёкшим сроком."""
    async with db.pool.acquire() as conn:
        expired_subscriptions = await conn.fetch("""
            SELECT user_id, end_date FROM subscriptions WHERE end_date < NOW()
        """)

    for subscription in expired_subscriptions:
        user_id = subscription["user_id"]
        await deactivate_vpn(db, user_id)
        await bot.send_message(user_id, "Ваша подписка истекла. Продлите её, чтобы восстановить доступ.")

        logger.info(f"Подписка пользователя {user_id} завершена, VPN отключён.")
