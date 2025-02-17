import asyncpg
from loguru import logger

class Database:
    def __init__(self, config):
        self.config = config
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=self.config['DB_USER'],
            password=self.config['DB_PASSWORD'],
            database=self.config['DB_NAME'],
            host=self.config['DB_HOST']
        )
        logger.info('Подключение к базе данных установлено.')
    
    async def close(self):
        await self.pool.close()
        logger.info('Подключение к базе данных закрыто.')
    
    async def create_users_table(self):
        async with self.pool.acquire() as conn:
            await conn.execute(""" 
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    phone_number TEXT
                )
            """)
            logger.info('Таблица users успешно создана.')

    async def create_tariffs_table(self):
        async with self.pool.acquire() as conn:
            await conn.execute(""" 
                CREATE TABLE IF NOT EXISTS tariffs (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price DECIMAL NOT NULL,
                    description TEXT
                )
            """)
            logger.info('Таблица tariffs успешно создана.')

    async def create_subscriptions_table(self):
        async with self.pool.acquire() as conn:
            await conn.execute(""" 
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    tariff_id INT NOT NULL,
                    start_date TIMESTAMP NOT NULL,
                    end_date TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id),
                    FOREIGN KEY (tariff_id) REFERENCES tariffs (id)
                )
            """)
            logger.info('Таблица subscriptions успешно создана.')

    async def add_tariff(self, name, price, description):
        async with self.pool.acquire() as conn:
            await conn.execute(""" 
                INSERT INTO tariffs (name, price, description) 
                VALUES ($1, $2, $3)
            """, name, price, description)
            logger.info(f'Тариф {name} добавлен в базу данных.')
    
    async def create_vpn_keys_table(self):
        async with self.pool.acquire() as conn:
            await conn.execute(""" 
                CREATE TABLE IF NOT EXISTS vpn_keys (
                    user_id BIGINT PRIMARY KEY,
                    key TEXT,
                    expiration_date TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id)
                )
            """)
            logger.info('Таблица vpn_keys успешно создана.')
