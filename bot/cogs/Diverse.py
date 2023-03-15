import logging
from discord.ext import commands
from discord import app_commands, Interaction, Object
from discord.app_commands import Choice
from utils.riotApiRessources import LANGUAGES

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

    @app_commands.command(name="setup_language", description="Setup the language used for the scheduler")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        language="The language used for the scheduler",
    )
    @app_commands.choices(
        language=[Choice(name=lang, value=val) for lang, val in LANGUAGES.items()]
    )
    async def setup_language(self, ctx: Interaction, language: str):
        _logger.info(f"setup_language command used by {ctx.user} with language {language}")
        await ctx.response.send_message("Language changed successfully !", ephemeral=True)


async def setup(bot: Setup):
    await bot.add_cog(Diverse(bot), guilds=[Object(id=bot.guild_id)])
