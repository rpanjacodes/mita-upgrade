import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

class Database:
    def __init__(self):
        self.pool = None
        self.dsn = os.getenv("DATABASE_URL")

    async def connect(self):
        if not self.dsn:
            raise ValueError("DATABASE_URL is not set in the environment.")
        self.pool = await asyncpg.create_pool(self.dsn)
        print("[✅] Database connected")

    async def close(self):
        if self.pool:
            await self.pool.close()
            print("[❌] Database connection closed")

    async def init_tables(self):
        await self.pool.execute("""
            CREATE TABLE IF NOT EXISTS special_users (
                user_id BIGINT PRIMARY KEY
            );
        """)
        print("[🛠️] Tables ensured")

    # ---- User Functions ----
    async def add_special_user(self, user_id: int):
        await self.pool.execute(
            "INSERT INTO special_users (user_id) VALUES ($1) ON CONFLICT DO NOTHING;",
            user_id
        )

    async def remove_special_user(self, user_id: int):
        await self.pool.execute(
            "DELETE FROM special_users WHERE user_id = $1;",
            user_id
        )

    async def is_special_user(self, user_id: int) -> bool:
        result = await self.pool.fetchrow(
            "SELECT 1 FROM special_users WHERE user_id = $1;",
            user_id
        )
        return result is not None

    async def list_special_users(self):
        return await self.pool.fetch("SELECT user_id FROM special_users;")
