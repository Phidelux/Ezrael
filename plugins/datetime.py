from core.plugin import Plugin
import datetime

class Datetime(Plugin):
    def on_command(self, message):
        if message.cmd[0] not in ['time', 'date', 'datetime']:
            return

        now = datetime.datetime.now()

        if message.cmd[0] == 'time':
            self.send_message(now.strftime("%H:%M"), message.channel)
        elif message.cmd[0] == 'date':
            self.send_message(now.strftime("%A, %d. %B %Y"), message.channel)
        elif message.cmd[0] == 'datetime':
            self.send_message(now.strftime("%A, %d. %B %Y - %H:%M"), message.channel)
