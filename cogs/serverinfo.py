import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Prefix command
    @commands.command(name="serverinfo", aliases=["guildinfo"])
    async def serverinfo_prefix(self, ctx):
        await self.send_info(ctx, ctx.guild)

    # Slash command
    @app_commands.command(name="serverinfo", description="View detailed information about this server")
    async def serverinfo_slash(self, interaction: discord.Interaction):
        await self.send_info(interaction, interaction.guild)

    async def send_info(self, ctx_or_interaction, guild: discord.Guild):
        if not guild:
            return  # Likely used in a DM

        total_members = guild.member_count
        bots = sum(1 for m in guild.members if m.bot)
        humans = total_members - bots

        text_channels = len([c for c in guild.text_channels])
        voice_channels = len([c for c in guild.voice_channels])
        categories = len([c for c in guild.categories])

        roles_sorted = sorted(guild.roles, key=lambda r: r.position, reverse=True)
        top_roles = [r.mention for r in roles_sorted if not r.is_default()][0:5]
        top_roles_text = ', '.join(top_roles) if top_roles else "None"

        boost_count = guild.premium_subscription_count or 0
        boost_level = guild.premium_tier

        created_at = discord.utils.format_dt(guild.created_at, style='F')

        embed = discord.Embed(
            title=f"Server Info - {guild.name}",
            description="Here's everything I found!",
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)

        embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
        embed.add_field(name="👑 Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="📅 Created On", value=created_at, inline=False)

        embed.add_field(name="👥 Members", value=f"Total: {total_members}\nHumans: {humans}\nBots: {bots}", inline=True)
        embed.add_field(name="📢 Channels", value=f"Text: {text_channels}\nVoice: {voice_channels}\nCategories: {categories}", inline=True)

        embed.add_field(name="🎭 Roles", value=f"{len(guild.roles)} total\nTop: {top_roles_text}", inline=False)
        embed.add_field(name="🚀 Boosts", value=f"Level {boost_level} ({boost_count} boosts)", inline=True)
        embed.set_footer(text=f"Requested at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")

        if isinstance(ctx_or_interaction, commands.Context):
            await ctx_or_interaction.send(embed=embed)
        else:
            await ctx_or_interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
