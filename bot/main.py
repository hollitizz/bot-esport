import discord
from discord.ext import commands, tasks
import os
import inspect
import aiohttp
import logging
import cogs

from utils.esportRequests import EsportRequests
from utils.SQLRequests import SQLRequests
from events import onReady, onMemberJoin, onMemberLeave
from utils.cleanSaveFolder import cleanSaveFolder
from utils.exportDatabase import exportDataBase


discord.utils.setup_logging()

class Setup(commands.Bot):
    def __init__(self):
        self.bot_id: int = int(os.getenv("BOT_ID"))
        self.token: str = os.getenv("TOKEN")
        self.guild_id: int = int(os.getenv("GUILD_ID"))
        super().__init__(command_prefix="!", intents=discord.Intents.all(), application_id=self.bot_id)
        self.db = SQLRequests()
        self.api = EsportRequests()

    async def setup_hook(self):
        self.session = aiohttp.ClientSession
        for cogName, cog in inspect.getmembers(cogs):
            if inspect.isclass(cog):
                logging.info(f"Loading {cogName} commands...")
                await self.load_extension(f"cogs.{cogName}")
                await self.tree.sync(guild=discord.Object(id=self.guild_id))
                logging.info(f"{cogName} commands loaded!")
        if self.db is not None:
            self.exportDataBaseTask.start()


    @tasks.loop(hours=1)
    async def exportDataBaseTask(self):
        exportDataBase()
        cleanSaveFolder()

    @exportDataBaseTask.before_loop
    async def before_exportDataBaseTask(self):
        await self.wait_until_ready()

    async def on_ready(self):
        await onReady.onReady(self)

    async def on_member_join(self, member: discord.Member):
        await onMemberJoin.onMemberJoin(self, member)

    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent):
        await onMemberLeave.onMemberLeave(self, payload)


def main():
    try:
        bot = Setup()
        bot.run(bot.token, reconnect=True, log_handler=None)
    except KeyboardInterrupt:
        logging.info("\nExiting...")
        exportDataBase()
        bot.session.close()
        bot.db.close()

if __name__ == "__main__":
    main()

