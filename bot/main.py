from Bot import Bot
import logging
from utils import loggingConfig


loggingConfig.setupLogging()


def main():
    try:
        bot = Bot()
        bot.run(bot.token, reconnect=True, log_handler=None)
    except KeyboardInterrupt:
        logging.info("\nExiting...")
        bot.session.close()
        bot.db.close()


if __name__ == "__main__":
    main()
