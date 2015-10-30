__author__ = 'ole'
from core.plugin import Plugin

# This plugin is necessary to keep the connection alive.


class Pong(Plugin):
    def on_ping(self, message):
        print("NOTICE: PONG {0}".format(message.content))
        self.send("PONG {0}\r\n".format(message.content).encode())
