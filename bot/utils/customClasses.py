
class dbGuild:
    def __init__(
        self,
        guild_id: str,
        language: str,
        followed_leagues: str,
        scheduler_channel: str,
        last_message: str,
    ):
        self.id = guild_id
        self.language = language
        self.followed_leagues = followed_leagues.split(',')
        self.scheduler_channel = scheduler_channel
        self.last_message = last_message
