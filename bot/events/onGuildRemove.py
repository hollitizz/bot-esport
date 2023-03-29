
from discord import Guild
from utils.types import BotType


async def onGuildRemove(self: BotType, guild: Guild):
    self.db.deleteGuild(guild.id)