import discord
from discord.ext import commands
import asyncio
import os
from db import connect_db, init_db
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")  # Secure your token in .env

# Setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.voice_states = True
intents.bans = True

# Bot setup: Prefix + Slash
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# Ready event
@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Game("「 M.I.T.A For You ❤️ 」")
    )
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

# On server join message
@bot.event
async def on_guild_join(guild: discord.Guild):
    embed = discord.Embed(
        title="Thanks for adding me! 🌟",
        description=(
            "I'm M.I.T.A – your multi-purpose companion bot! 🎉\n\n"
            "▶ Use `/help` to explore features.\n"
            "▶ Want chat? Use `/set_channel`.\n\n"
            "Let’s grow your server together!"
        )
    )
    embed.set_footer(text="Made With ❤️ By Kirtikaze Team")

    # Try sending to system channel or first available channel
    if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
        await guild.system_channel.send(embed=embed)
    else:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
                break

# Load all cogs from /cogs/
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Loaded cog: {filename}")
            except Exception as e:
                print(f"❌ Failed to load cog {filename}: {e}")

# Bot main
async def main():
    await connect_db()
    await init_db()
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
