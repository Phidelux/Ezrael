from core.plugin import Plugin
import codecs

class Base64(Plugin):
    def on_command(self, message):
        # Check if topic change request was sent.
        if message.cmd[0] != 'base64':
            return

        msg = message.content[self.context['command_prefix_len'] + len(message.cmd[0]):].strip()
        self.send_message(codecs.encode(bytes(msg.strip(), 'utf-8'), "base64").decode(), message.channel)
