from gmusic import Client
import requests
import hashlib


def cmd_dl(bot, update, groups):
    DlCommand(groups[0]).execute(bot, update)


class DlCommand(object):
    def __init__(self, song_nid):
        self.client = Client()
        self.song_nid = song_nid

    @staticmethod
    def song_download(song_url):
        response = requests.get(song_url)

        if response.status_code == requests.codes.ok:
            filename = hashlib.md5(song_url).hexdigest()
            filepath = "/tmp/{}.mp3".format(filename)

            f = open(filepath, 'wb')
            f.write(response.content)
            f.close()

            return dict(filename=filename, filepath=filepath)
        return None

    def execute(self, bot, update):
        update.message.reply_text('downloading...')

        song_url = self.client.get_song_url(self.song_nid)
        song_file = self.song_download(song_url)

        if song_file is not None:
            audio = open(song_file['filepath'], 'rb')
            bot.send_audio(
                chat_id=update.message.chat_id,
                audio=audio,
                caption=u'Take it!'
            )
        else:
            update.message.reply_text(song_url)