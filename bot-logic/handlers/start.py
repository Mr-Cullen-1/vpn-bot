from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.main_menu import get_main_menu
from keyboards.device_selection import get_device_selection_keyboard
from db import Database
from services.vpn_keys import generate_vpn_key_and_config  

def register_start_handlers(dp: Dispatcher, db: Database, bot):
    @dp.message(Command('start'))
    async def start_command(message: Message):
        user_id = message.from_user.id
        full_name = message.from_user.full_name
        
        # Извлечение реферального ID из команды
        referrer_user_id = None
        if len(message.text.split()) > 1:
            referrer_user_id = message.text.split()[1]  # Это пример, адаптировать под нужды

        async with db.pool.acquire() as conn:
            # Проверка, зарегистрирован ли уже пользователь
            user = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", user_id)
            
            if user:
                # Если пользователь уже есть, проверим наличие VPN ключа
                vpn_key = await conn.fetchval("SELECT key FROM vpn_keys WHERE user_id = $1", user_id)
                
                if vpn_key:
                    await message.answer(
                        f'Привет, {full_name}! Ваш VPN-ключ уже активен. Продолжайте использование.\n'
                        "Выберите один из вариантов ниже:",
                        reply_markup=get_main_menu()
                    )
                else:
                    # Генерация нового VPN-ключа, если его нет
                    await generate_vpn_key_and_config(db, user_id, message.bot)
                    await message.answer(
                        f"Привет, {full_name}! Ваш новый VPN-ключ был сгенерирован.\n"
                        "Вот ваш конфигурационный файл для подключения.\n"
                        "Теперь выберите тариф для дальнейшего использования.",
                        reply_markup=get_main_menu()
                    )
            else:
                # Если пользователя нет в базе, добавляем его
                await conn.execute(
                    'INSERT INTO users (telegram_id, full_name) VALUES ($1, $2)',
                    user_id, full_name
                )

                # Если был реферер, сохраняем информацию о том, кто пригласил
                if referrer_user_id:
                    referrer_user_id = int(referrer_user_id)  # Преобразуем в int
                    await conn.execute(
                        'INSERT INTO referrals (user_id, referrer_user_id) VALUES ($1, $2)',
                        user_id, referrer_user_id
                    )

                await message.answer(
                    f"Добро пожаловать, {full_name}! Для продолжения выберите устройство для подключения.",
                    reply_markup=get_device_selection_keyboard()
                )

# Пример регистрации обработчика:
# register_start_handlers(dp, db, bot)
