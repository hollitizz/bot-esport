from discord import Interaction
from utils.types import BotType


async def setupLanguage(self: BotType, ctx: Interaction, language: str):
    self.db.updateGuildPreferredLanguage(ctx.guild_id, language)
    await ctx.response.send_message(
        "Language updated successfully !",
        ephemeral=True
    )