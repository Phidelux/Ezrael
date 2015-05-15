from core.plugin import Plugin

class HereAmI(Plugin):
    def onMsg(self, irc, channel, nick, msg):
        if 'ezrael' in msg.lower():
            irc.sendMessage2Channel('Here am I!', channel)
