from discord import Guild
from utils.types import BotType


async def onGuildJoin(self: BotType, guild: Guild):
    self.db.createGuild(guild.id)
    try:
        await guild.system_channel.send(
            "Hello, I'm the scheduler bot for the League of Legends tournaments !\n"
            "To use me, you must first setup the scheduler with the command `/setup_scheduler`.\n"
            "You can also use the command `/setup_language` to setup the language of the days of the schedule.\n"
        )
    except Exception:
        pass