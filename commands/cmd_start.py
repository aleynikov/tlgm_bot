def cmd_start(bot, update):
    StartCommand().execute(bot, update)


class StartCommand(object):
    def __init__(self):
        pass

    def execute(self, bot, update):
        update.message.reply_text('')
