import logging
from datetime import datetime, timedelta
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHANNEL_ID = "jacobs_music"  

TARIFFS = {
    "1_month": {"duration": "1 месяц", "price": 199},
    "3_months": {"duration": "3 месяца", "price": 499},
    "6_months": {"duration": "6 месяцев", "price": 899},
    "1_year": {"duration": "12 месяцев", "price": 1399},
}


def create_telegram_stars_payment_link(amount, description="Подписка на тариф"):
    """Создание ссылки на оплату через Telegram Stars"""
    payment_link = f"https://t.me/{CHANNEL_ID}?start=pay_{amount}"
    return payment_link


async def handle_telegram_stars_payment(callback: types.CallbackQuery, tariff_key: str, bot, db):
    """Обработчик для платежей через Telegram Stars"""
    tariff = TARIFFS.get(tariff_key.strip())
    if not tariff:
        await callback.message.edit_text("Выбранный тариф не найден. Пожалуйста, попробуйте снова.")
        return

    duration = tariff["duration"]
    amount = tariff["price"]

    payment_link = create_telegram_stars_payment_link(amount)

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


async def activate_subscription(user_id, tariff_key, bot, db):
    """Активировать подписку для пользователя в базе данных"""
    tariff = TARIFFS.get(tariff_key)
    if not tariff:
        return

    duration_days = {
        "1_month": 30,
        "3_months": 90,
        "6_months": 180,
        "1_year": 365,
    }.get(tariff_key, 30)

    async with db.pool.acquire() as conn:
        await conn.execute(""" 
            INSERT INTO subscriptions (user_id, tariff_id, start_date, end_date)
            VALUES ($1, $2, $3, $4)
        """, user_id, tariff_key, datetime.now(), datetime.now() + timedelta(days=duration_days))

    await bot.send_message(user_id, f"Ваша подписка на {tariff['duration']} активирована! Спасибо за оплату.")
