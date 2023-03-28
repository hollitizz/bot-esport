import logging
import discord

from utils.types import Setup

async def onReady(self: Setup):
    await self.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="https://lolesports.com/"
        )
    )
    logging.info(f"{self.user} is Ready !")
