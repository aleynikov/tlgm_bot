from telegram.ext import Updater, CommandHandler
import logging
import config
import commands

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def error_handler(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(config.telegram['access_token'])

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', commands.cmd_start))
    dp.add_handler(CommandHandler('random_girl', commands.cmd_randomgirl))
    dp.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
