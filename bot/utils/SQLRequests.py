from mysql.connector import MySQLConnection
from mysql.connector.connection import CursorBase
import os


class SQLRequests(MySQLConnection):
    def __init__(self):
        super().__init__(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        self.__cursor: CursorBase = self.cursor()

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