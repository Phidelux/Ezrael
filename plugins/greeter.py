from core.plugin import Plugin
import re

class Greeter(Plugin):
    def onMsg(self, irc, channel, nick, msg):
      # Define the greetiungs pattern.
      pattern = re.compile('[hH][eE3aA4][lL1]{2}[oO0]|[mM][oO0][iI][nN]|[oO0][lL1]{1,2}[eE3aA4]')

      if nick == "Avedo" and pattern.match(msg) != None:
         irc.sendMessage2Channel( ("Greetings Master"), channel )
      elif pattern.match(msg) != None:
         irc.sendMessage2Channel( ("Hello, " + nick), channel )
      elif msg == "duck":
         irc.sendMessage2Channel( '__("<', channel )
         irc.sendMessage2Channel( '\__/', channel )
         irc.sendMessage2Channel( ' ^^', channel )
         irc.sendMessage2Channel( "DUCKTALES UhhhHuuuuuuu", channel )