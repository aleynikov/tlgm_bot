#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

import ConfigParser
import random

from libs.photo.photo_collector import get_top_photos, photo_download

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)

def random_photo(bot, update):
	links = get_top_photos(10)
	link = random.choice(links)

	result = photo_download(link)

	if result != None:
		photo_file = open(result['filepath'], 'rb')
		bot.sendPhoto(chat_id=update.message.chat_id, photo=photo_file, caption=u'Take it!')
	else:
		update.message.reply_text(link)

def echo(bot, update):
	update.message.reply_text(update.message.text)

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	cfg = ConfigParser.ConfigParser()
	cfg.read('../cfg/telegram.cfg')

	updater = Updater(cfg.get('api', 'access_token'))

	dp = updater.dispatcher

	dp.add_handler(MessageHandler([Filters.text], echo))
	dp.add_handler(CommandHandler('random_girl', random_photo))

	dp.add_error_handler(error)

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
