import logging
import aiohttp
import hashlib
import base64
import json
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CRYPTOMUS_API_URL = "https://api.cryptomus.com/v1/invoice/create"
API_KEY = "ce84b0cbaca0ea2d354c8992d6a830480bb568da"
USER_ID = "12b256a7-1d69-4340-9365-cec2e20d3557"  

TARIFFS = {
    "1_month": {"duration": "1 месяц", "price": 199},
    "3_months": {"duration": "3 месяца", "price": 499},
    "6_months": {"duration": "6 месяцев", "price": 899},
    "1_year": {"duration": "12 месяцев", "price": 1399},
}

def generate_signature(payload, api_key):
    """Генерация подписи для запроса"""
    payload_json = json.dumps(payload)
    base64_payload = base64.b64encode(payload_json.encode()).decode()
    sign = hashlib.md5((base64_payload + api_key).encode()).hexdigest()
    return sign

async def create_crypto_payment_link(amount, description="Подписка на тариф"):
    """Создание ссылки на оплату через Cryptomus"""
    payload = {
        "amount": amount,  # Сумма в рублях
        "currency": "RUB",  # В валюте рубли
        "order_desc": description,  # Описание
        "return_url": "https://t.me/vpnprojbot",  # URL для возврата после оплаты
    }
    
    sign = generate_signature(payload, API_KEY)
    
    headers = {
        "user_id": USER_ID,
        "sign": sign,
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{CRYPTOMUS_API_URL}v1/invoice/create", json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("status") == "success":
                    payment_url = data.get("invoice_url")  
                    return payment_url
            else:
                logger.error(f"Ошибка при создании ссылки на оплату: {response.status} - {await response.text()}")
            return None

async def handle_payment(callback: types.CallbackQuery, tariff_key: str, bot, db):
    """Обработчик для платежей через Cryptomus"""
    
    tariff = TARIFFS.get(tariff_key)
    if not tariff:
        await callback.message.edit_text("Выбранный тариф не найден. Пожалуйста, попробуйте снова.")
        return

    duration = tariff["duration"]
    amount = tariff["price"]
    payment_link = await create_crypto_payment_link(amount)
    if payment_link:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[ 
            [InlineKeyboardButton(text=f"Оплатить {amount}₽ ({duration})", url=payment_link)],
            [InlineKeyboardButton(text="Назад", callback_data="main_menu")]
        ])
        await callback.message.edit_text(
            text=f"Вы выбрали тариф на {duration}.\n"
                 f"Сумма: {amount}₽.\n\n"
                 f"Перейдите по кнопке ниже для завершения оплаты.",
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text("Не удалось создать ссылку для оплаты. Попробуйте позже.")
