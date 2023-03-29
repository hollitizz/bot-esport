import datetime
from io import BytesIO

import discord
from utils.planningFormattor import getFormattedPlanning

from utils.types import BotType


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


async def sendPlanning(self: BotType):
    for guild in self.db.getGuilds():
        g = self.get_guild(int(guild.id))
        if g is None:
            self.db.deleteGuild(guild.id)
            return
        channel = g.get_channel(int(guild.scheduler_channel))
        if channel is None:
            self.db.updateGuildSchedulerChannel(guild.id, None)
            return
        if guild.last_message is not None:
            try:
                message = await channel.fetch_message(int(guild.last_message))
                await message.delete()
            except discord.errors.NotFound:
                pass
        schedules = self.api.getSchedules(
            guild.language, guild.followed_leagues
        ).get('data', {}).get('schedule', {}).get('events', [])
        planning = getFormattedPlanning(
            guild.language,
            guild.timezone,
            getSchedulesByDayOnCurrentWeek(schedules)
        )
        with BytesIO() as image_binary:
            planning.save(image_binary, 'PNG')
            image_binary.seek(0)
            new_message = await channel.send(file=discord.File(fp=image_binary, filename='planning.png'))
            self.db.updatePlanningLastMessage(guild.id, new_message.id)


async def refreshPlanning(self: BotType):
    for guild in self.db.getGuilds():
        g = self.get_guild(int(guild.id))
        if g is None:
            self.db.deleteGuild(guild.id)
            return
        channel = g.get_channel(int(guild.scheduler_channel))
        if channel is None:
            self.db.updateGuildSchedulerChannel(guild.id, None)
            return
        message = None
        if guild.last_message is not None:
            try:
                message = await channel.fetch_message(int(guild.last_message))
            except discord.errors.NotFound:
                message = None
        if message is None:
            await sendPlanning(self)
            return
        schedules = self.api.getSchedules(
            guild.language, guild.followed_leagues
        ).get('data', {}).get('schedule', {}).get('events', [])
        planning = getFormattedPlanning(
            guild.language,
            guild.timezone,
            getSchedulesByDayOnCurrentWeek(schedules),
        )
        with BytesIO() as image_binary:
            planning.save(image_binary, 'PNG')
            image_binary.seek(0)
            await message.edit(attachments=[discord.File(fp=image_binary, filename='planning.png')])
