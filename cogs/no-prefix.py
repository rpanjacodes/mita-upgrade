import discord
from discord.ext import commands
import asyncpg

# Replace with your Discord user ID
BOT_OWNER_ID = 123456789012345678  # <-- 🔒 Your ID goes here

class NoPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def insert_user(self, user_id: int):
        async with self.bot.db.acquire() as conn:
            await conn.execute("INSERT INTO special_users (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Skip bots and DMs
        if message.author.bot or not message.guild:
            return

        # Only allow the bot owner
        if message.author.id != BOT_OWNER_ID:
            return

        # Command: add_user <user_id>
        if message.content.startswith("add_user "):
            try:
                parts = message.content.split()
                if len(parts) != 2:
                    return await message.channel.send("❌ Usage: `add_user <user_id>`")

                user_id = int(parts[1])
                await self.insert_user(user_id)
                await message.channel.send(f"✅ User `{user_id}` added to special_users.")
            except Exception as e:
                await message.channel.send(f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(NoPrefix(bot))
