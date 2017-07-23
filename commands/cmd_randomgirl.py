from random import choice
import requests
import config
import pytumblr
import hashlib


def cmd_randomgirl(bot, update):
    RandomGirlCommand().execute(bot, update)


class RandomGirlCommand(object):
    def __init__(self):
        self.client = pytumblr.TumblrRestClient(
            config.thumblr['consumer_key'],
            config.thumblr['consumer_secret'],
            config.thumblr['oauth_token'],
            config.thumblr['oauth_secret'],
        )

    def get_photo_links(self):
        posts = self.client.posts(
            blogname=config.thumblr['post'],
            type='photo',
            limit=config.thumblr['posts_limit'],
        )
        links = []
        for post in posts['posts']:
            photos = post['photos']

            for photo in photos:
                # collect origin photo url
                links.append(photo['original_size']['url'])
        return links

    def photo_download(self, photo_url):
        response = requests.get(photo_url)

        if response.status_code == requests.codes.ok:
            filename = hashlib.md5(photo_url).hexdigest()
            filepath = "/tmp/{}.jpg".format(filename)

            f = open(filepath, 'wb')
            f.write(response.content)
            f.close()

            return dict(filename=filename, filepath=filepath)
        return None

    def execute(self, bot, update):
        photo_links = self.get_photo_links()

        if photo_links:
            photo_link = choice(photo_links)
            photo_file = self.photo_download(photo_link)

            if photo_file is not None:
                photo = open(photo_file['filepath'], 'rb')
                bot.sendPhoto(
                    chat_id=update.message.chat_id,
                    photo=photo,
                    caption=u'Take it!'
                )
            else:
                update.message.reply_text(photo_link)
