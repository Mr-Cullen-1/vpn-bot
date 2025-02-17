from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_device_selection_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Windows 🖥", callback_data="device_windows"),
            InlineKeyboardButton(text="Android 📱", callback_data="device_android")
        ],
        [
            InlineKeyboardButton(text="iPhone 📱", callback_data="device_ios"),
            InlineKeyboardButton(text="macOS 💻", callback_data="device_macos")
        ]
    ])
    return keyboard
