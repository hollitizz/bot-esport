import logging
from discord.ext import commands
from discord import app_commands, Interaction, Object

from commands.esport import setupPlanningSender

from utils.types import Setup

_logger = logging.getLogger(__name__)


class Esport(commands.Cog, description="Command group for esport commands"):
    def __init__(self, bot: Setup):
        self.bot = bot

    @app_commands.command(
        name="setup_scheduler",
        description="Setup the scheduler who will send the schedule of requested leagues for next week"
    )
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        channel="The id or the name of channel where the schedule will be sent",
    )
    async def setup_scheduler(self, ctx: Interaction, channel: str):
        _logger.info(f"Command setup_scheduler executed by {ctx.user}")
        await setupPlanningSender.setupPlanningSender(self.bot, ctx, channel)

    @setup_scheduler.error
    async def setup_scheduler_error(self, ctx: Interaction, error):
        _logger.error(f"{ctx.user} got:\n{error}")
        if isinstance(error, commands.MissingPermissions):
            await ctx.response.send_message(
                "You don't have the permission to use this command, you must be able to manage messages",
                ephemeral=True
            )
        else:
            await ctx.response.send_message("An error occured", ephemeral=True)

async def setup(bot: Setup):
    await bot.add_cog(Esport(bot))
