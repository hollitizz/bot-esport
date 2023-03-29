import discord
import logging
from utils.types import BotType

_logger = logging.getLogger(__name__)

async def onMemberJoin(self: BotType, member: discord.Member):
    _logger.info(f"User \"{member}\" joined the server")