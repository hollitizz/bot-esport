from utils.riotApiRequests import riotApiRequests
from utils.SQLRequests import SQLRequests
from events import onReady, onMemberJoin, onMemberLeave, onGuildJoin, onGuildRemove
from utils.exportDatabase import exportDataBase
from utils.sendPlanning import sendPlanning, refreshPlanning
import cogs
import os
import inspect
import aiohttp
import asyncio
import datetime
import discord
from discord.ext import commands, tasks
import logging
import pytz


_tz = pytz.timezone('Europe/Paris')
_logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self):
        self.bot_id: int = int(os.getenv("BOT_ID"))
        self.token: str = os.getenv("TOKEN")
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(), application_id=self.bot_id
        )
        self.db = SQLRequests()
        self.api = riotApiRequests()

    async def setup_hook(self):
        self.session = aiohttp.ClientSession
        _logger.info("Loading commands...")
        for cogName, cog in inspect.getmembers(cogs):
            if inspect.isclass(cog):
                await self.load_extension(f"cogs.{cogName}")
        await self.tree.sync()
        _logger.info("Commands loaded")
        self.exportDataBaseTask.start()
        self.send_planning.start()
        self.refresh_planning.start()

    @tasks.loop(hours=168)
    async def send_planning(self):
        await sendPlanning(self)

    @send_planning.before_loop
    async def before_send_planning(self):
        await self.wait_until_ready()
        now = datetime.datetime.now(_tz)
        day = now.weekday()
        target = now + datetime.timedelta(days=7 - day)
        target = target.replace(hour=8, minute=0, second=0, microsecond=0)
        delta = target - now
        _logger.info(f"Waiting {round(delta.total_seconds())} seconds ({target.strftime('%d/%m/%Y, %H:%M:%S')}) before sending planning")
        await asyncio.sleep(delta.total_seconds())

    @tasks.loop(hours=24)
    async def refresh_planning(self):
        if datetime.datetime.now(_tz).weekday() == 0:
            return
        await refreshPlanning(self)

    @refresh_planning.before_loop
    async def before_refresh_planning(self):
        await self.wait_until_ready()
        now = datetime.datetime.now(_tz)
        target = now + datetime.timedelta(days=1)
        target = target.replace(hour=0, minute=0, second=0, microsecond=0)
        delta = target - now
        _logger.info(f"Waiting {round(delta.total_seconds())} seconds ({target.strftime('%d/%m/%Y, %H:%M:%S')}) before refreshing planning")
        await asyncio.sleep(delta.total_seconds())

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

    async def on_guild_join(self, guild: discord.Guild):
        await onGuildJoin.onGuildJoin(self, guild)

    async def on_guild_remove(self, guild: discord.Guild):
        await onGuildRemove.onGuildRemove(self, guild)
