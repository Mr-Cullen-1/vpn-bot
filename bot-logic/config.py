import os
from dotenv import load_dotenv


load_dotenv()

def load_config():
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "DB_HOST": os.getenv("DB_HOST", "localhost"),
        "DB_POST": os.getenv("DB_PORT", 5432),
        "DB_NAME": os.getenv("DB_NAME", "vpn_bot"),
        "DB_USER": os.getenv("DB_USER", "vpn_user"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD", "secure_password")
    }
