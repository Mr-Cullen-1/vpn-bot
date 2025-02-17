from aiogram import Dispatcher
from db import Database
from handlers.start import register_start_handlers
from handlers.menu import register_menu_handlers

def register_handlers(dp: Dispatcher, db: Database, bot):
    register_start_handlers(dp, db, bot)
    register_menu_handlers(dp, db, bot)  
