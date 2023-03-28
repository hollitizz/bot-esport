import asyncio
import datetime
import discord
from discord.ext import commands, tasks
import os
import inspect
import aiohttp
import logging
import cogs

from utils.riotApiRequests import riotApiRequests
from utils.SQLRequests import SQLRequests
from events import onReady, onMemberJoin, onMemberLeave
from utils.exportDatabase import exportDataBase
from utils.sendPlanning import sendPlanning, refreshPlanning


discord.utils.setup_logging()

class Setup(commands.Bot):
    def __init__(self):
        self.bot_id: int = int(os.getenv("BOT_ID"))
        self.token: str = os.getenv("TOKEN")
        self.guild_id: int = int(os.getenv("GUILD_ID"))
        super().__init__(command_prefix="!", intents=discord.Intents.all(), application_id=self.bot_id)
        self.db = SQLRequests()
        self.api = riotApiRequests()

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
            self.send_planning.start()
            self.refresh_planning.start()

    @tasks.loop(hours=168)
    async def send_planning(self):
        await sendPlanning(self)

    @send_planning.before_loop
    async def before_send_planning(self):
        await self.wait_until_ready()
        now = datetime.datetime.now()
        day = now.weekday()
        target = now + datetime.timedelta(days=7 - day)
        target = target.replace(hour=8, minute=0, second=0, microsecond=0)
        delta = target - now
        await asyncio.sleep(delta.seconds)


    @tasks.loop(hours=24)
    async def refresh_planning(self):
        await refreshPlanning(self)

    @refresh_planning.before_loop
    async def before_refresh_planning(self):
        await self.wait_until_ready()
        now = datetime.datetime.now()
        target = now + datetime.timedelta(days=1)
        target = target.replace(hour=0, minute=0, second=0, microsecond=0)
        delta = target - now
        await asyncio.sleep(delta.seconds)

    @tasks.loop(hours=1)
    async def exportDataBaseTask(self):
        exportDataBase()

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
        bot.session.close()
        bot.db.close()

if __name__ == "__main__":
    main()

