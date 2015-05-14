from core.plugin import Plugin
from core.colors import Color
import random

class Rainbow(Plugin):
  def onMsg(self, irc, channel, nick, msg):
    # Ensure that the given message starts with a command.
    if msg[0] != '!':
      return

    # Extract the current command and message ...
    command = msg[1:].split()[0].strip().lower()
    message = msg[len(command)+1:].strip()

    # ... and print the colorized version.
    if command == "black":
      irc.sendMessage2Channel("{0}{1}".format(Color.black, message), channel )
    elif command == "blue":
      irc.sendMessage2Channel("{0}{1}".format(Color.navy_blue, message), channel )
    elif command == "green":
      irc.sendMessage2Channel("{0}{1}".format(Color.green, message), channel )
    elif command == "red":
      irc.sendMessage2Channel("{0}{1}".format(Color.red, message), channel )
    elif command == "brown":
      irc.sendMessage2Channel("{0}{1}".format(Color.brown, message), channel )
    elif command == "purple":
      irc.sendMessage2Channel("{0}{1}".format(Color.purple, message), channel )
    elif command == "olive":
      irc.sendMessage2Channel("{0}{1}".format(Color.olive, message), channel )
    elif command == "yellow":
      irc.sendMessage2Channel("{0}{1}".format(Color.yellow, message), channel )
    elif command == "lime_green":
      irc.sendMessage2Channel("{0}{1}".format(Color.lime_green, message), channel )
    elif command == "teal":
      irc.sendMessage2Channel("{0}{1}".format(Color.teal, message), channel )
    elif command == "aqua_light":
      irc.sendMessage2Channel("{0}{1}".format(Color.aqua_light, message), channel )
    elif command == "royal_blue":
      irc.sendMessage2Channel("{0}{1}".format(Color.royal_blue, message), channel )
    elif command == "hot_pink":
      irc.sendMessage2Channel("{0}{1}".format(Color.hot_pink, message), channel )
    elif command == "dark_gray":
      irc.sendMessage2Channel("{0}{1}".format(Color.dark_gray, message), channel )
    elif command == "light_gray":
      irc.sendMessage2Channel("{0}{1}".format(Color.light_gray, message), channel )
    elif command == "white":
      irc.sendMessage2Channel("{0}{1}".format(Color.white, message), channel )
    elif command == "bold":
      irc.sendMessage2Channel("{0}{1}".format(Color.bold, message), channel )
    elif command == "italic":
      irc.sendMessage2Channel("{0}{1}".format(Color.italic, message), channel )
    elif command == "underline":
      irc.sendMessage2Channel("{0}{1}".format(Color.underline, message), channel )
    elif command == "underline2":
      irc.sendMessage2Channel("{0}{1}".format(Color.underline2, message), channel )
    elif command == "reverse":
      irc.sendMessage2Channel("{0}{1}".format(Color.reverse, message), channel )
    elif command == "strike":
      irc.sendMessage2Channel("{0}{1}".format(Color.strike_through, message), channel )
    elif command == "rainbow" and message != '':
      rainbowMsg = ''
      for i in range(0, len(message)):
        rainbowMsg += "{0}{1}".format(Color.random(), message[i])
      rainbowMsg += "{0}".format(Color.clear)
      irc.sendMessage2Channel(rainbowMsg, channel)
    elif command == "rainbow":
      irc.sendMessage2Channel(
        "I love {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}!".format(
          Color.black, 'R', Color.navy_blue, 'A', Color.green, 'I', 
          Color.red, 'N', Color.purple, 'B', Color.yellow, 'O', 
          Color.teal, 'W', Color.hot_pink, 'S', Color.clear
        ), channel)