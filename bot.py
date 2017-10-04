from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler, Filters
import logging
import config
import commands
from conversation import Conversation


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def error_handler(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def conv_handler(bot, update):
    conv = Conversation()

    name_str = 'chat_{chat_id}'.format(chat_id=update.message.chat_id)
    conv.set_session(name_str)

    conv.make_question(update.message.text)
    answer = conv.get_answer()
    if answer:
        update.message.reply_text(answer)


def main():
    updater = Updater(config.telegram['access_token'])

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', commands.cmd_start))
    dp.add_handler(CommandHandler('rand_girl', commands.cmd_randomgirl))
    dp.add_handler(CommandHandler('gmusic', commands.cmd_gmusic))
    dp.add_handler(RegexHandler(r'/dl_([0-9a-z]+)', commands.cmd_dl, pass_groups=True))
    dp.add_handler(MessageHandler(Filters.text, conv_handler))
    dp.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
