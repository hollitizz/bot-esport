import logging
import os
from discord.ext import commands
from discord import Object, app_commands, Interaction

from utils.types import BotType

from utils import sendPlanning

_logger = logging.getLogger(__name__)


class Admin(commands.Cog, description="Groupe de commande Divers"):
    def __init__(self, bot: BotType):
        self.bot = bot

    @app_commands.command(name="force_refresh_planning", description="Répond avec \"Pong !\"")
    async def forceRefreshPlanning(self, ctx: Interaction):
        _logger.info(f"Commande force_refresh_planning exécutée par {ctx.user}")
        await ctx.response.defer(ephemeral=True, thinking=True)
        await sendPlanning.refreshPlanning(self.bot)
        await ctx.edit_original_response(content="Planning refreshed !")

async def setup(bot: BotType):
    await bot.add_cog(Admin(bot), guild=Object(id=os.getenv("ADMIN_GUILD_ID")))
