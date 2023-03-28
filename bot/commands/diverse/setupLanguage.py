import logging
from discord import Interaction
from main import Setup


async def setupLanguage(self: Setup, ctx: Interaction, language: str):
    self.db.updateGuildPreferredLanguage(ctx.guild_id, language)
    await ctx.response.send_message(
        "Language updated successfully !",
        ephemeral=True
    )