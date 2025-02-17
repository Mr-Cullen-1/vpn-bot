from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text='🧨Подключить VPN', callback_data='view_tariffs')
    builder.button(text='🔑 Мой ключ', callback_data='my_vpn_key') 
    builder.button(text='🛠 Инструкция', callback_data='instructions')
    builder.button(text='🎁Пригласить друга', callback_data='referrals')
    builder.button(text='✏️ Сообщить о проблеме', callback_data='help')
    builder.adjust(2)
    return builder.as_markup()
