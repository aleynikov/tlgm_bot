from telegram.ext import Dispatcher, MessageHandler, Filters
from telegram import ParseMode
from gmusic import Client


def cmd_gmusic(bot, update):
    GMusicCommand().execute(bot, update)


class GMusicCommand(object):
    def __init__(self):
        self.client = Client()
        self.msg_handler = MessageHandler(Filters.text, self.search)
        self.dp = Dispatcher.get_instance()

    def search(self, bot, update):
        result = self.client.search_songs(update.message.text)
        songs_tpl = []
        for song in result:
            songs_tpl.append(u'*{}*\n{}\n_Download:_ /dl\_{}'.format(
                song['artist'],
                song['title'],
                song['nid']))

        if len(songs_tpl) > 0:
            update.message.reply_text(text='\n\n'.join(songs_tpl), parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text('Hm... nothing to found.')
        self.dp.remove_handler(self.msg_handler)

    def execute(self, bot, update):
        update.message.reply_text('Please enter here a song title.')
        self.dp.add_handler(self.msg_handler)