import logging
from discord.ext import commands
from discord import app_commands, Interaction, Object

from utils.types import Setup

from commands.diverse import ping, help

_logger = logging.getLogger(__name__)


class Diverse(commands.Cog, description="Groupe de commande Divers"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(name="ping", description="Répond avec \"Pong !\"")
    async def ping(self, ctx: Interaction):
        _logger.info(f"Commande ping exécutée par {ctx.user}")
        await ping.ping(ctx)

    @app_commands.command(name="help", description="Display help menu")
    async def help(self, ctx: Interaction):
        await help.help(self.bot, ctx)


async def setup(bot: Setup):
    await bot.add_cog(Diverse(bot), guilds=[Object(id=bot.guild_id)])
