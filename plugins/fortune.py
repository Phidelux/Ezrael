from core.plugin import Plugin
import urllib.request


class Fortune(Plugin):
    def on_command(self, irc, message):
        if message.cmd[0] != 'fortune':
            return

        # Setup the request url, ...
        url = 'http://www.iheartquotes.com/api/v1/random' \
              + '?show_permalink=false' \
              + '&max_characters=200' \
              + '&format=text'

        # ... fetch a fortune from http://iheartquotes.com, ...
        fortune = urllib.request.urlopen(url).read()

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

        for (k, v) in special.items():
            fortune = fortune.replace(k, v)

        # ... and send it as message to the irc channel.
        irc.send_message('[Fortune] ' + fortune, message.channel)
