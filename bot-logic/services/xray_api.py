import aiohttp
import json
from loguru import logger

XRAY_API_URL = "http://127.0.0.1:443"

HEADERS = {
    "Content-Type": "application/json"
}

async def add_user(uuid, email="default@example.com"):
    """Добавляет нового пользователя в Xray."""
    url = f"{XRAY_API_URL}/xray/api/inbounds/addClient"
    payload = {
        "id": uuid,
        "email": email,
        "alterId": 0,
        "level": 0
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=HEADERS, json=payload) as response:
            data = await response.text()
            if response.status == 200:
                logger.info(f"Пользователь {email} (UUID: {uuid}) добавлен в Xray.")
                return True
            else:
                logger.error(f"Ошибка при добавлении пользователя: {data}")
                return False

async def remove_user(uuid):
    """Удаляет пользователя из Xray."""
    url = f"{XRAY_API_URL}/xray/api/inbounds/removeClient"
    payload = {"id": uuid}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=HEADERS, json=payload) as response:
            data = await response.text()
            if response.status == 200:
                logger.info(f"Пользователь с UUID {uuid} удалён из Xray.")
                return True
            else:
                logger.error(f"Ошибка при удалении пользователя: {data}")
                return False

async def get_users():
    """Получает список пользователей из Xray."""
    url = f"{XRAY_API_URL}/xray/api/inbounds/getClients"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                users = await response.json()
                return users
            else:
                logger.error(f"Ошибка при получении списка пользователей: {await response.text()}")
                return None
