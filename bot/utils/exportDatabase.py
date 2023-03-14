from datetime import date
from logging import getLogger
import os
import subprocess


_logger = getLogger(__name__)


def exportDataBase():
    today = date.today().strftime("%d-%m-%Y")
    subprocess.Popen(
        f"mysqldump -p'{os.getenv('DB_ROOT_PASS')}' -h {os.getenv('DB_HOST')} {os.getenv('DB_NAME')} > ./db/db_saves/{today}.sql;"
        f"rm -rf ./db/init.sql; cp ./db/db_saves/{today}.sql ./db/init.sql",
        shell=True
    )
    _logger.info(f"save done at ./db_saves/{today}.sql")