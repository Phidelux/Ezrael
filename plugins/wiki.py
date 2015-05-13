from core.plugin import Plugin
import DNS

class Wiki(Plugin):
    def onMsg(self, irc, channel, nick, msg):
        # Make sure an actual command was sent.
        if str(msg[0]) != '!' or str(msg[1:5]).lower() != 'wiki':
            return

        # Fetch an answer from wikipedia, ...
        wiki = self.wiki(command[1:]) \
            .replace('\r', '') \
            .replace('\n', ' ') \
            .replace('\t', ' ')

        # ... replace special characters ...
        special = {
            '&nbsp;': ' ', '&amp;': '&', '&quot;': '"',
            '&lt;': '<', '&gt;': '>'
        }

        for (k,v) in special.items():
            wiki = wiki.replace(k, v)

        # ... and send it as message to the irc channel.
        irc.sendMessage2Channel('[Wikipedia] ' + wiki, channel)

    def wiki(self, query):
        query = '_'.join(query).strip().replace(' \t\r\n', '_')
        host = query + '.wp.dg.cx'
        result = ''

        DNS.DiscoverNameServers()
        request = DNS.Request(host, qtype=DNS.Type.TXT, protocol='tcp')
        reply = request.req()
        reply.show()

        if reply.answers:
            for answer in reply.answers:
                print(answer['data'])

        return result