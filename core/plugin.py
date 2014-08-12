class Plugin(object):
    def __init__(self, config=None):
        self.config = config

    def init(self, irc):
        pass

    def onJoin(self, irc, channel, nick, msg):
        pass

    def onRecv(self, irc, msg):
        pass

    def onMsg(self, irc, channel, nick, msg):
        pass

    def onPrivMsg(self, irc, channel, nick, msg):
        pass

    def onNotice(self, irc, channel, nick, msg):
        pass