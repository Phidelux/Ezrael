from core.plugin import Plugin
import urllib

class Fortune(Plugin):
    def onMsg(self, irc, channel, nick, msg):
        # Make sure an actual command was sent.
        if str(msg[0]) != '!' or len(msg.split()) == 0:
            return

        # Make the command case insensitive.
        command = str(msg[1:]).lower()

        # Break the command into pieces.
        command = command.split()

        if command[0] == 'fortune':
            # Setup the request url, ...
            iheartquotes = 'http://www.iheartquotes.com/api/v1/random' \
                           + '?show_permalink=false' \
                           + '&max_characters=200' \
                           + '&format=text'

            # ... fetch a fortune from http://iheartquotes.com, ...
            fortune = urllib.request.urlopen(iheartquotes).read()

            # ... remove linebreaks and tabs, ...
            fortune = str(fortune, 'utf-8') \
                .replace('\r', '') \
                .replace('\n', ' ') \
                .replace('\t', ' ')

            # ... replace special characters ...
            special = {
                '&nbsp;': ' ', '&amp;': '&', '&quot;': '"',
                '&lt;': '<', '&gt;': '>'
            }

            for (k,v) in special.items():
                fortune = fortune.replace(k, v)

            # ... and send it as message to the irc channel.
            irc.sendMessage2Channel('[Fortune] ' + fortune, channel)
