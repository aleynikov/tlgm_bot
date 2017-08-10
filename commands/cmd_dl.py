from gmusic import Client
import requests
import hashlib
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, APIC, error


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

    def __bind_tags(self, song_file, song_info):
        audio = MP3(song_file['filepath'], ID3=ID3)

        try:
            audio.add_tags()
        except error:
            pass

        # title
        audio.tags.add(
            TIT2(
                encoding=3,
                text=unicode(song_info['title'])
            )
        )

        # artist
        audio.tags.add(
            TPE1(
                encoding=3,
                text=unicode(song_info['artist'])
            )
        )

        # album cover
        response = requests.get(song_info['albumArtRef'][0]['url'])
        with open('/tmp/{0}.cover.jpg'.format(song_file['filename']), 'wb') as out:
            out.write(response.content)

        audio.tags.add(
            APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc=u'Cover',
                data=open('/tmp/{0}.cover.jpg'.format(song_file['filename']), 'rb').read()
            )
        )

        audio.save(v2_version=3)


    def execute(self, bot, update):
        update.message.reply_text('downloading...')

        song_url = self.client.get_song_url(self.song_nid)
        song_file = self.song_download(song_url)
        song_info = self.client.get_song_info(self.song_nid)

        self.__bind_tags(song_file, song_info)

        if song_file is not None:
            audio = open(song_file['filepath'], 'rb')
            bot.send_audio(
                chat_id=update.message.chat_id,
                audio=audio,
                caption=u'Take it!'
            )
        else:
            update.message.reply_text(song_url)