import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Prefix command
    @commands.command(name="avatar")
    async def avatar_prefix(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await self.send_avatar(ctx, member)

    # Slash command
    @app_commands.command(name="avatar", description="Get a user's avatar")
    @app_commands.describe(user="The user to get avatar of")
    async def avatar_slash(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        await self.send_avatar(interaction, user)

    async def send_avatar(self, ctx_or_interaction, member):
        avatar_url = member.display_avatar.url

        embed = discord.Embed(
            title=f"{member.display_name}'s Avatar",
            description="Click the button below to download the avatar.",
        )
        embed.set_image(url=avatar_url)

        view = View()
        view.add_item(Button(label="Download Avatar", url=avatar_url))

        if isinstance(ctx_or_interaction, commands.Context):
            await ctx_or_interaction.send(embed=embed, view=view)
        else:
            await ctx_or_interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Avatar(bot))
