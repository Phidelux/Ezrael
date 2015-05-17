from core.plugin import Plugin
import datetime

class Datetime(Plugin):
  def onMsg(self, irc, channel, nick, msg):
    # Prepare the message ...
    msg = msg.strip().lower()

    # ... and ensure an actual command was sent.
    if msg not in ['!time', '!date', '!datetime']:
      return

    # ... otherwise fetch the current date and time.
    now = datetime.datetime.now()

    if msg == '!time':
      # Generate the formated string and return it.
      irc.sendMessage2Channel(now.strftime("%H:%M"), channel)
    elif msg == '!date':
      # Generate the formated string and return it.
      irc.sendMessage2Channel(now.strftime("%A, %d. %B %Y"), channel)
    elif msg == '!datetime':
      # Generate the formated string and return it.
      irc.sendMessage2Channel(now.strftime("%A, %d. %B %Y - %H:%M"), channel)