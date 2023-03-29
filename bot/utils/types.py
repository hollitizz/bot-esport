from discord.ext import commands
import discord
import os
from utils.riotApiRequests import riotApiRequests

from utils.SQLRequests import SQLRequests

class BotType(commands.Bot, SQLRequests):
    def __init__(self):
        self.bot_id: int = int(os.getenv("BOT_ID"))
        self.token: str = os.getenv("TOKEN")
        super().__init__(command_prefix="!", intents=discord.Intents.all(), application_id=self.bot_id)
        self.db = SQLRequests()
        self.db = None
        self.api = riotApiRequests()