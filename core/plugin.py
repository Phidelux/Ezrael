class Plugin(object):
    def __init__(self, config=None):
        self.config = config

    def init(self, irc):
        pass

    def on_receive(self, irc, message):
        pass

    def on_private_message(self, irc, message):
        pass

    def on_channel_message(self, irc, message):
        pass

    def on_message(self, irc, message):
        pass

    def on_command(self, irc, message):
        pass

    def on_kick(self, irc, message):
        pass

    def on_join(self, irc, message):
        pass

    def on_ping(self, irc, message):
        pass

    def on_notice(self, irc, message):
        pass
