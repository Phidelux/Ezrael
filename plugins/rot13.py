from core.plugin import Plugin
import codecs

class Rot13(Plugin):
    def on_command(self, message):
        # Check if topic change request was sent.
        if message.cmd[0] != 'rot13':
            return

        msg = message.content[self.context['command_prefix_len'] + len(message.cmd[0]):].strip()
        self.send_message(codecs.encode(msg, "rot-13"), message.channel)
