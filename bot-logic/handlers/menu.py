from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.main_menu import get_main_menu
from payment_methods import payment_card, payment_crypto, payment_stars
import logging

logging.basicConfig(level=logging.INFO)

TARIFFS = {
    "1_month": {"duration": "1 месяц", "price": 199},
    "3_months": {"duration": "3 месяца", "price": 499},
    "6_months": {"duration": "6 месяцев", "price": 899},
    "1_year": {"duration": "12 месяцев", "price": 1399}
}

async def send_vpn_key(callback: CallbackQuery, db):
    """Отправка пользователю его VPN-ключа"""
    user_id = callback.from_user.id

    async with db.pool.acquire() as conn:
        vpn_key = await conn.fetchval("SELECT key FROM vpn_keys WHERE user_id = $1", user_id)

    if vpn_key:
        await callback.message.answer(f"Ваш VPN ключ:\n<code>{vpn_key}</code>", parse_mode="HTML")
    else:
        await callback.message.answer("У вас нет активного VPN ключа. Оформите подписку, чтобы получить его.")

    await callback.answer()

def get_back_button(callback_data: str) -> InlineKeyboardButton:
    """Создание кнопки "Назад"."""
    return InlineKeyboardButton(text='Назад', callback_data=callback_data)

def register_menu_handlers(dp: Dispatcher, db, bot):
    """Регистрируем все обработчики меню"""

    @dp.callback_query(lambda c: c.data == "my_vpn_key")
    async def my_vpn_key_handler(callback: CallbackQuery):
        await send_vpn_key(callback, db)

    @dp.callback_query(lambda c: c.data == "instructions")
    async def instructions(callback: CallbackQuery):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[get_back_button("main_menu")]])
        await callback.message.edit_text(
            "Я помогу вам с подключением VPN!\n"
            "Вот что я могу сделать:\n"
            "- Выбрать тариф\n"
            "- Активировать пробный период\n"
            "- Уведомить о подписке\n\n"
            "Просто используйте кнопки в меню.",
            reply_markup=keyboard
        )

    @dp.callback_query(lambda c: c.data == "main_menu")
    async def back_to_main_menu(callback: CallbackQuery):
        await callback.message.edit_text(
            "Добро пожаловать в главное меню!\nВыберите один из вариантов ниже:",
            reply_markup=get_main_menu()
        )

    @dp.callback_query(lambda c: c.data == "view_tariffs")
    async def view_tariffs(callback: CallbackQuery):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1 месяц - 199₽", callback_data="tariff_1_month")],
            [InlineKeyboardButton(text="3 месяца - 499₽", callback_data="tariff_3_months")],
            [InlineKeyboardButton(text="6 месяцев - 899₽", callback_data="tariff_6_months")],
            [InlineKeyboardButton(text="12 месяцев - 1399₽", callback_data="tariff_1_year")],
            [get_back_button("main_menu")]
        ])
        await callback.message.edit_text("Выберите тарифный план:", reply_markup=keyboard)

    @dp.callback_query(lambda c: c.data.startswith("tariff_"))
    async def tariff_selection(callback: CallbackQuery):
        tariff_key = callback.data.replace("tariff_", "").strip()
        logging.info(f"Выбранный тариф: {tariff_key}")

        tariff = TARIFFS.get(tariff_key)
        if not tariff:
            await callback.message.edit_text(
                "Тариф не найден. Пожалуйста, выберите тариф снова.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[get_back_button("view_tariffs")]])
            )
            return

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳Банковская карта", callback_data=f"payment_card_{tariff_key}")],
            [InlineKeyboardButton(text="💰Криптовалюта", callback_data=f"payment_crypto_{tariff_key}")],
            [InlineKeyboardButton(text="🌟Телеграмм старс", callback_data=f"payment_stars_{tariff_key}")],
            [get_back_button("view_tariffs")]
        ])
        await callback.message.edit_text(
            text=f"Вы выбрали тариф на {tariff['duration']}.\n"
                 f"Стоимость: {tariff['price']}₽.\n\n"
                 f"Пожалуйста, выберите способ оплаты:",
            reply_markup=keyboard
        )

    @dp.callback_query(lambda c: c.data.startswith("payment_"))
    async def payment_selection(callback: CallbackQuery):
        payment_data = callback.data.split("_")
        payment_method = payment_data[1]
        tariff_key = "_".join(payment_data[2:]).strip()
        logging.info(f"Выбран способ оплаты: {payment_method}, тариф: {tariff_key}")

        tariff = TARIFFS.get(tariff_key)
        if not tariff:
            await callback.message.edit_text("Тариф не найден. Пожалуйста, выберите тариф снова.")
            return

        if payment_method == "card":
            await payment_card.handle_payment(callback, tariff["price"], bot, db)
        elif payment_method == "crypto":
            await payment_crypto.handle_payment(callback, tariff_key, bot, db)
        elif payment_method == "stars":
            await payment_stars.handle_telegram_stars_payment(callback, tariff_key, bot, db)

    @dp.callback_query(lambda c: c.data == "referrals")
    async def handle_referrals(callback: CallbackQuery):
        user_id = callback.from_user.id
        referral_link = f"https://t.me/vpnprojbot?start={user_id}"

        # Отправляем пользователю реферальную ссылку
        await callback.message.answer(
            f"Вот ваша реферальная ссылка: {referral_link}\nПоделитесь ей с друзьями!"
        )
        await callback.answer()