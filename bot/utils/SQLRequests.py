import logging
from mysql.connector import MySQLConnection
from mysql.connector.connection import CursorBase
import os

from utils.customClasses import dbGuild

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

    def createGuild(self, guild_id: int):
        request = f"""
            INSERT INTO guilds (id)
            VALUES ("{guild_id}")
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        _logger.info(f"Created guild: {guild_id}")

    def deleteGuild(self, guild_id: int):
        request = f"""
            DELETE FROM guilds
            WHERE id = "{guild_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        _logger.info(f"Deleted guild: {guild_id}")

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
        _logger.info(f"Updating guild: {guild_id} preferred language to: {language}")
        request = f"""
            UPDATE guilds
            SET language = "{language}"
            WHERE id = "{guild_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        _logger.info(f"Updated guild: {guild_id} preferred language to: {language}")

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

    def updatePlanningLastMessage(self, guild_id: int, new_message_id: int):
        request = f"""
            UPDATE guilds
            SET last_message = "{new_message_id}"
            WHERE id = "{guild_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        _logger.info(f"Updated guild: {guild_id} last message id to: {new_message_id}")

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

    def getGuilds(self) -> list[dbGuild]:
        request = f"""
            SELECT * FROM guilds
            WHERE scheduler_channel IS NOT NULL AND followed_leagues IS NOT NULL
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return [dbGuild(*i) for i in self.__cursor.fetchall()]