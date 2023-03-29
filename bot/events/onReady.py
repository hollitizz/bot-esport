import logging
import discord

from utils.types import BotType

_logger = logging.getLogger(__name__)

async def onReady(self: BotType):
    await self.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="https://lolesports.com/"
        )
    )
    _logger.info(f"{self.user} is Ready !")
