from core.plugin import Plugin
import random

class EightBall(Plugin):
    fortunes = [
        "Yes", "No", "Maybe", "Not yet", "Only time will tell",
        "I have no idea", "Absolutely", "Ask again later"
    ]

    def on_message(self, message):
        if message.cmd[0] == "8ball":
            self.send_message(EightBall.fortunes[random.randint(0, len(EightBall.fortunes) - 1)], message.channel)
