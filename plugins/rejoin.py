from core.plugin import Plugin


class Rejoin(Plugin):
    def on_kick(self, message):
        print("NOTICE: I was kicked by {0} from {1}\r\n".format(message.nick, message.channel))
        self.join_channel(message.channel)
        print("NOTICE: Rejoining {0} ...".format(message.channel))
        self.send("MODE {0} -o {1} \r\n".format(message.channel, message.nick).encode())
