from discord import Interaction
from main import Setup


async def setupLanguage(self: Setup, ctx: Interaction, language: str):
    if ctx.guild.id not in [guild.id for guild in self.db.getGuilds()]:
        self.db.createGuild(ctx.guild.id)
    self.db.updateGuildPreferredLanguage(ctx.guild_id, language)
    await ctx.response.send_message(
        "Language updated successfully !",
        ephemeral=True
    )