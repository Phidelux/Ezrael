from core.plugin import Plugin
import random
import re

class RollDice(Plugin):
  def onMsg(self, irc, channel, nick, msg):
    # Make sure an actual command was sent.
    if str(msg[0]) != '!' or (str(msg[1:9]).lower() != 'rolldice' and str(msg[1:5]).lower() != 'dice'):
      return

    # Define default values.
    numEyes = 6
    numRoles = 1

    # Define the number pattern ...
    pattern = re.compile(r"(?<![-.])\b[0-9]+\b(?!\.[0-9])")

    # ... and search for numbers in the command.
    matches = pattern.findall(msg)

    if len(matches) > 1:
      numEyes = max([2, int(matches[0])])
      numRoles = max([1, int(matches[1])])
    elif len(matches) > 0:
      numEyes = max([2, int(matches[0])])

    if numEyes == 42:
      irc.sendMessage2Channel("This is the Answer to The Ultimate Question of Life, the Universe, and Everything!", channel)
    elif numEyes != 20 or numRoles > 1:
      results = [];
      for i in range(0, numRoles):
        results.append(str(random.randint(1, numEyes)))

      irc.sendMessage2Channel(", ".join(results), channel)
    else:
      result = random.randint(1, numEyes)

      if result == 1:
        irc.sendMessage2Channel("1 -> CRITICAL!", channel)
      elif result == 20:
        irc.sendMessage2Channel("20 -> FLOP! YOU GET BEATEN UP!", channel)
      else:
        irc.sendMessage2Channel("{0}".format(result), channel)
