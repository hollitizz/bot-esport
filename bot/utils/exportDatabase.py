from datetime import date
from logging import getLogger
import os
import subprocess


_logger = getLogger(__name__)


def exportDataBase():
    today = date.today().strftime("%d-%m-%Y")
    subprocess.Popen(
        f"mysqldump -p'{os.getenv('DB_ROOT_PASS')}' -h {os.getenv('DB_HOST')} {os.getenv('DB_NAME')} > ./db/db_saves/{today}.sql;"
        f"rm -rf ./db/db_saves/init.sql; cp ./db/db_saves/{today}.sql ./db/db_saves/init.sql",
        shell=True
    )
    _logger.info(f"save done at ./db/db_saves/{today}.sql")