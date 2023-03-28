import datetime
from io import BytesIO
import json
import logging

from discord import Embed
import discord
from utils.planningFormattor import getFormattedPlanning

from utils.types import Setup

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


def getSchedulesByDayOnCurrentWeek(schedules: list[dict]):
    today = datetime.date.today()
    startOfWeek = today - datetime.timedelta(days=today.weekday())
    weekSchedules = [startOfWeek]
    weekSchedules.extend([startOfWeek + datetime.timedelta(days=i)
                         for i in range(1, 7)])
    weekGames: dict[str, list[dict]] = {}
    for schedule in schedules:
        date = datetime.date.fromisoformat(
            schedule.get('startTime', '').split('T')[0])
        if date in weekSchedules:
            weekGames.setdefault(date.isoformat(), []).append(schedule)
    return weekGames


async def sendScheduler(self: Setup):
    for guild in self.db.getGuilds():
        g = self.get_guild(int(guild.id))
        if g is None:
            self.db.deleteGuild(guild.id)
            return
        channel = g.get_channel(int(guild.scheduler_channel))
        if channel is None:
            self.db.updateGuildSchedulerChannel(guild.id, None)
            return
        schedules = self.api.getSchedules(
            guild.language, guild.followed_leagues
        ).get('data', {}).get('schedule', {}).get('events', [])
        planning = getFormattedPlanning(
            'fr-FR',
            getSchedulesByDayOnCurrentWeek(schedules)
        )
        with BytesIO() as image_binary:
            planning.save(image_binary, 'PNG')
            image_binary.seek(0)
            await channel.send(file=discord.File(fp=image_binary, filename='planning.png'))
