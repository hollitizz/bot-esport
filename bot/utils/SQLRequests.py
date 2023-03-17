import logging
from mysql.connector import MySQLConnection
from mysql.connector.connection import CursorBase
import os

_logger = logging.getLogger(__name__)

class SQLRequests(MySQLConnection):
    def __init__(self):
        _logger.info("Connecting to database...")
        super().__init__(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        self.__cursor: CursorBase = self.cursor()
        _logger.info("Database connected!")

    def __clearCache(self):
        self.connect()
        try:
            self.__cursor.fetchall()
        except:
            pass

    def getTables(self) -> 'list[str]':
        request = f"""
            SHOW TABLES
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return [i[0] for i in self.__cursor.fetchall()]

    def getGuildPreferredLanguage(self, guild_id: int) -> str:
        request = f"""
            SELECT language
            FROM guilds
            WHERE id = "{guild_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return self.__cursor.fetchone()[0]

    def updateGuildPreferredLanguage(self, guild_id: int, language: str):
        request = f"""
            UPDATE guilds
            SET language = "{language}"
            WHERE id = "{guild_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        _logger.info(f"Updated guild: {guild_id} preferred language to: {language}")

    def getGuildSchedulerChannel(self, guild_id: int) -> str:
        request = f"""
            SELECT scheduler_channel
            FROM guilds
            WHERE id = "{guild_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return self.__cursor.fetchone()[0]

    def updateGuildSchedulerChannel(self, guild_id: int, channel_id: int):
        request = f"""
            UPDATE guilds
            SET scheduler_channel = "{channel_id}"
            WHERE id = "{guild_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        _logger.info(f"Updated guild: {guild_id} scheduler channel to channel: {channel_id}")

    def getGuildFollowedLeagues(self, guild_id: int) -> list[str]:
        request = f"""
            SELECT followed_leagues
            FROM guilds
            WHERE id = "{guild_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return self.__cursor.fetchone()[0].split(",")

    def updateGuildFollowedLeagues(self, guild_id: int, leagues: list[str]):
        request = f"""
            UPDATE guilds
            SET followed_leagues = "{','.join(leagues)}"
            WHERE id = "{guild_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        _logger.info(f"Updated guild: {guild_id} followed leagues to: {','.join(leagues)}")
