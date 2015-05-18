from core.plugin import Plugin


class HereAmI(Plugin):
    def on_message(self, irc, message):
        if len(message.cmd) == 0 and 'ezrael' in message.content.lower():
            irc.send_message('Here am I!', message.channel)

    def on_join(self, irc, message):
        if message.nick == irc.ircNick:
            irc.send_message('Here am I!', message.channel)
