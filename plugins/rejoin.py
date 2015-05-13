from core.plugin import Plugin
import urllib.request
import time

class Rejoin(Plugin):
    def onKick(self, irc, channel, nick, msg):
        print ('******* !!! - I was kicked by ' + nick + ' from ' + channel + '\r\n')
        irc.joinChannel(channel)
        print ('******* Rejoining ...' + channel)
        irc.sendPlain("MODE {0} -o {1} \r\n".format(channel, nick).encode())