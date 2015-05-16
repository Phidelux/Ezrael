from core.plugin import Plugin
import urllib.request
import time

class Rejoin(Plugin):
    def onKick(self, irc, channel, nick, msg):
        print ("NOTICE: I was kicked by {0} from {1}\r\n".format(nick, channel))
        irc.joinChannel(channel)
        print ("NOTICE: Rejoining {0} ...".format(channel))
        irc.sendPlain("MODE {0} -o {1} \r\n".format(channel, nick).encode())