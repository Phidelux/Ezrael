from core.plugin import Plugin
from core.colors import Color

class EasterEgg(Plugin):
  def onMsg(self, irc, channel, nick, msg):
    # Ensure that the given message starts with a command.
    if msg[0] != '!':
      return

    # Extract the current command.
    command = msg[1:].split()[0].strip().lower()

    if command == "moo":
      irc.sendMessage2Channel("MOO yourself, " + nick, channel )
    elif command == "xkcd":
      irc.sendMessage2Channel("https://c.xkcd.com/random/comic/", channel)
    elif command == "train":
      irc.sendMessage2Channel("Choo Choo! It's the Mystery Train!", channel )
    elif command == "poo":
      irc.sendMessage2Channel("Don't be a potty mouth", channel )
    elif command == "rainbow":
      irc.sendMessage2Channel(
        "I love {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}!".format(
          Color.bold_black, 'R', Color.bold_blue, 'A', Color.bold_green, 'I', 
          Color.bold_red, 'N', Color.bold_violet, 'B', Color.bold_yellow, 'O', 
          Color.bold_cyan, 'W', Color.bold_white, 'S', Color.bold_black
        ), channel )
    elif command == "duck":
      irc.sendMessage2Channel("__(\"<", channel )
      irc.sendMessage2Channel("\__/", channel )
      irc.sendMessage2Channel(" ^^", channel )
      irc.sendMessage2Channel("DUCKTALES UhhhHuuuuuuu", channel )
    elif command == "duckduck":
      irc.sendMessage2Channel(".......ENTE......:", channel )
      irc.sendMessage2Channel(":       ,~~.     :", channel )
      irc.sendMessage2Channel("E      (  6 )-_, E", channel )
      irc.sendMessage2Channel("N (\___ )=='-'   N", channel )
      irc.sendMessage2Channel("T  \ .   ) )     T", channel )
      irc.sendMessage2Channel("E   \ `-' /      E", channel )
      irc.sendMessage2Channel(": ~~'`~'`~'`~`~' :", channel )
      irc.sendMessage2Channel(":......ENTE......:", channel )