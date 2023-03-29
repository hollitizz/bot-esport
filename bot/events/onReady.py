import logging
import discord

from utils.types import Setup

_logger = logging.getLogger(__name__)

async def onReady(self: Setup):
    await self.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="https://lolesports.com/"
        )
    )
    _logger.info(f"{self.user} is Ready !")
