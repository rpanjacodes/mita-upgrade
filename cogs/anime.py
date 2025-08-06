import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

MAL_CLIENT_ID = "your_client_id_here"  # 🔑 Replace with your real MAL client ID

class AnimeSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="anime_search", description="Search anime info from MyAnimeList")
    @app_commands.describe(anime_name="Name of the anime")
    async def anime_search(self, interaction: discord.Interaction, anime_name: str):
        await interaction.response.defer(thinking=True)

        headers = {
            "X-MAL-CLIENT-ID": MAL_CLIENT_ID
        }

        url = (
            f"https://api.myanimelist.net/v2/anime?q={anime_name}"
            "&limit=1&fields=id,title,main_picture,synopsis,mean,episodes,genres,start_date,status"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    return await interaction.followup.send("⚠️ Failed to fetch anime info from MyAnimeList.")

                data = await response.json()
                if not data.get("data"):
                    return await interaction.followup.send("❌ No anime found.")

                anime = data["data"][0]["node"]

                embed = discord.Embed(
                    title=anime["title"],
                    description=anime.get("synopsis", "No synopsis available.")
                )

                if "main_picture" in anime:
                    embed.set_image(url=anime["main_picture"].get("large", anime["main_picture"].get("medium")))

                embed.add_field(name="📺 Episodes", value=str(anime.get("episodes", "N/A")), inline=True)
                embed.add_field(name="⭐ Score", value=str(anime.get("mean", "N/A")), inline=True)
                embed.add_field(name="📅 Aired", value=anime.get("start_date", "N/A"), inline=True)
                embed.add_field(name="📡 Status", value=anime.get("status", "N/A"), inline=True)

                genres = ", ".join(g["name"] for g in anime.get("genres", []))
                embed.add_field(name="🎭 Genres", value=genres or "N/A", inline=False)

                embed.set_footer(text="Data provided by MyAnimeList")

                await interaction.followup.send(embed=embed)

    @app_commands.command(name="anime_character", description="Search anime character info (waifu/husbando)")
    @app_commands.describe(name="Name of the character")
    async def anime_character(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer(thinking=True)

        url = f"https://api.jikan.moe/v4/characters?q={name}&limit=1"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return await interaction.followup.send("⚠️ Failed to fetch character info.")

                data = await response.json()
                if not data.get("data"):
                    return await interaction.followup.send("❌ No character found.")

                char = data["data"][0]

                embed = discord.Embed(
                    title=char["name"],
                    url=char["url"],
                    description=char.get("about", "No description available.")
                )

                if "images" in char and "jpg" in char["images"]:
                    embed.set_thumbnail(url=char["images"]["jpg"].get("image_url"))

                embed.add_field(name="❤️ Favorites", value=str(char.get("favorites", "N/A")), inline=True)
                embed.set_footer(text="Powered by Jikan | Data from MyAnimeList")

                await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AnimeSearch(bot))
