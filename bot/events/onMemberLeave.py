import discord
import logging
from utils.types import Setup

_logger = logging.getLogger(__name__)

async def onMemberLeave(self: Setup, payload: discord.RawMemberRemoveEvent):
    _logger.info(f"User \"{payload.user}\" leaved the server")