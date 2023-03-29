import discord
import logging
from utils.types import BotType

_logger = logging.getLogger(__name__)

async def onMemberLeave(self: BotType, payload: discord.RawMemberRemoveEvent):
    _logger.info(f"User \"{payload.user}\" leaved the server")