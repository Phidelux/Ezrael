from core.plugin import Plugin
import random

class HereAmI(Plugin):
    hereami = [
      "Are you talking to me?", "Talk to the hand!", "Here am I!", 
      "You wanna hug?", "Hello there!"
    ]

    def on_message(self, message):
        if len(message.cmd) == 0 and 'ezrael' in message.content.lower():
            hereMsg = HereAmI.hereami[random.randint(0, len(HereAmI.hereami) - 1)]
            self.send_message(hereMsg, message.channel)

    def on_join(self, message):
        if message.nick == irc.ircNick:
            self.send_message('Here am I!', message.channel)
