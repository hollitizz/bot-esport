
from discord import Guild
from utils.types import Setup


async def onGuildRemove(self: Setup, guild: Guild):
    self.db.deleteGuild(guild.id)