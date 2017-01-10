#!/usr/bin/env python

from telegram import (
	InlineKeyboardButton,
	InlineKeyboardMarkup
)

from telegram.ext import (
	Updater,
	CommandHandler,
	MessageHandler,
	Filters,
	CallbackQueryHandler
)

import logging

from libs.cfg import Cfg
import random

from libs.photo_collector import get_top_photos, photo_download

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

def photo_selection(bot, update):
	keyboard = [InlineKeyboardButton('Option 1', callback_data=1),
		InlineKeyboardButton('Option 2', callback_data=2)]

	reply_markup = InlineKeyboardMarkup(keyboard)

	update.message.reply_text('Please choose:', reply_markup=reply_markup)

def btn_photo_selection(bot, update):
	query = update.callback_query

	update.message.reply_text(query.data)

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	cfg = Cfg('telegram')

	updater = Updater(cfg.get('api', 'access_token'))

	dp = updater.dispatcher

	dp.add_handler(MessageHandler([Filters.text], echo))
	dp.add_handler(CommandHandler('random_girl', random_photo))
	dp.add_handler(CommandHandler('friday_girls', photo_selection))
	dp.add_handler(CallbackQueryHandler(btn_photo_selection))

	dp.add_error_handler(error)

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
