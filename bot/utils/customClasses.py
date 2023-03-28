import logging


class dbGuild:
    def __init__(
        self,
        guild_id: str,
        language: str,
        followed_leagues: str,
        scheduler_channel: str
    ):
        self.id = guild_id
        self.language = language
        self.followed_leagues = followed_leagues.split(',')
        self.scheduler_channel = scheduler_channel

    def __str__(self):
        return f"Guild: {self.id}, language: {self.language}, followed leagues: {self.followed_leagues}, scheduler channel: {self.scheduler_channel}"