from core.plugin import Plugin
import dns.resolver

class Wiki(Plugin):
    def onMsg(self, irc, channel, nick, msg):
        # Make sure an actual command was sent.
        if str(msg[0]) != '!' or len(msg.split()) == 0:
            return

        # Make the command case insensitive.
        command = str(msg[1:]).lower()

        # Break the command into pieces.
        command = command.split()

        if command[0] == 'wiki':
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
                fortune = fortune.replace(k, v)

            # ... and send it as message to the irc channel.
            irc.sendMessage2Channel('[Wikipedia] ' + wiki, channel)

    def wiki(self, query):
        query = '_'.join(query).strip().replace(' \t\r\n', '_')
        host = query + '.wp.dg.cx'
        result = ''

        try:
            answers = dns.resolver.query(host, 'TXT')

            for txtRecord in answers.response.answer:
                result = txtRecord.to_text().split('"')[1]
        except dns.resolver.NXDOMAIN:
            print('No such domain %s' % host)
        except dns.resolver.Timeout:
            print('Timed out while resolving %s' % host)
        except dns.exception.DNSException:
            print('Unhandled exception')
        return result