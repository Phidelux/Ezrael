from core.plugin import Plugin
from bs4 import BeautifulSoup
import urllib.parse
import requests

# TODO apply new plugin-schema
# TODO fix plugin

class Wiki(Plugin):
    def onMsg(self, irc, channel, nick, msg):
        # Make sure an actual command was sent.
        if str(msg[0]) != '!' or str(msg[1:5]).lower() != 'wiki':
            return

        # Fetch the query string ...
        query = str(msg[5:])

        # ... and fetch the content object.
        wikiJson = self.fetch_wiki(query)
        wikiSoup = BeautifulSoup(str(wikiJson))

        redirect = self.check_redirect(wikiSoup)
        if (redirect != None):
            wikiJson = self.fetch_wiki(redirect)

        # Extract the content block ...
        content = wikiJson['parse']['text']['*']

        # ... and verify that this is not a redirect.
        wikiSoup = BeautifulSoup(content)

        redirect = wikiSoup.select('div.redirectMsg > ul > li > a')
        if len(redirect) > 0:
            target = "http://en.wikipedia.org/{0}".format(redirect[0]['href'])

        # ... and extract the abstract (eg. first paragraph).
        paragraphs = wikiSoup.find_all('p')

        abstract = BeautifulSoup('')
        if len(paragraphs) > 0:
            abstract = paragraphs[0]

        # Remove citations from the abstract, ...
        for cite in abstract.find_all('sup'):
            cite.string = ''

        # ... remove all html stuff ...
        beautyWiki = abstract.get_text()

        # ... and remove linebreaks and tabs.
        beautyWiki = beautyWiki.replace('\r', '') \
            .replace('\n', ' ') \
            .replace('\t', ' ')

        # ... and send it as message to the irc channel.
        self.send_message('[Wikipedia] ' + beautyWiki, channel)

    def check_redirect(self, content):
        # Check if the given content contains a redirect.
        redirect = content.select('div.redirectMsg > ul > li > a')
        if len(redirect) > 0:
            # If it contains a redirect extract the redirect title.
            target = redirect[0]['href']
            start = target.find('?title=') + 7
            end = target.find('&', start)
            return target[start:end]

        return None

    def prepare_url(self, query):
        # Define the query parameters, ...
        params = {"action": "parse", "prop": "text", "format": "json", "page": "{0}".format(urllib.parse.quote(query))}

        # ... encode the query parameters ...
        queryStr = "&".join("{0}={1}".format(k, v) for k, v in params.items())

        # ... and setup the request url.
        return "http://en.wikipedia.org/w/api.php?{0}".format(queryStr)

    def fetch_wiki(self, query):
        # Setup the request url ...
        wikiApi = self.prepare_url(query)

        # ... and fetch the english wikipedia from http://en.wikipedia.org/w/api.php.
        return requests.get(wikiApi).json()
