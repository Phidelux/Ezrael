from core.plugin import Plugin
import datetime


class Datetime(Plugin):
    def on_command(self, irc, message):
        if message.cmd[0] not in ['time', 'date', 'datetime']:
            return

        now = datetime.datetime.now()

        if message.cmd[0] == 'time':
            irc.send_message(now.strftime("%H:%M"), message.channel)
        elif message.cmd[0] == 'date':
            irc.send_message(now.strftime("%A, %d. %B %Y"), message.channel)
        elif message.cmd[0] == 'datetime':
            irc.send_message(now.strftime("%A, %d. %B %Y - %H:%M"), message.channel)
