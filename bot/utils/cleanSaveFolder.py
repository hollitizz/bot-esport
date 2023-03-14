
from time import sleep
from datetime import datetime
from logging import getLogger
import os
import subprocess

_logger = getLogger(__name__)

def cleanSaveFolder():
    while len(os.listdir("./db_saves")) > 7:
        oldest_file = min([datetime.strptime(f, "%d-%m-%Y.sql") for f in os.listdir("./db_saves") if f != "init.sql"])
        subprocess.Popen(
            f"rm -rf ./db_saves/{oldest_file.strftime('%d-%m-%Y')}.sql",
            stderr=subprocess.DEVNULL,
            shell=True
        )
        _logger.info(f"Oldest save: \"{oldest_file.strftime('%d-%m-%Y')}.sql\" deleted")
        sleep(0.5)