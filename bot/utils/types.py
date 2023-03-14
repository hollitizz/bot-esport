from discord.ext import commands
import discord
import os

from utils.SQLRequests import SQLRequests

class Setup(commands.Bot, SQLRequests):
    def __init__(self):
        self.bot_id: int = int(os.getenv("BOT_ID"))
        self.token: str = os.getenv("TOKEN")
        self.guild_id: int = int(os.getenv("GUILD_ID"))
        super().__init__(command_prefix="!", intents=discord.Intents.all(), application_id=self.bot_id)
        try :
            self.db = SQLRequests()
        except:
            self.db = None

