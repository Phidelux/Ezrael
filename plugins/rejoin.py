from core.plugin import Plugin


class Rejoin(Plugin):
    def on_kick(self, message):
        self.logger.info("I was kicked by {0} from {1}\r\n".format(message.nick, message.channel))
        self.join_channel(message.channel)
        self.logger.info("Rejoining {0} ...".format(message.channel))
        self.send("MODE {0} -o {1} \r\n".format(message.channel, message.nick).encode())
