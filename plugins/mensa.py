from core.plugin import Plugin
from core.colors import Color
import urllib.request, urllib.error
import traceback
import time
import json

class Mensa(Plugin):
    def on_command(self, message):
        if message.cmd[0] != 'mensa':
            return

        try:
            # Store the current date as string.
            today = time.strftime('%Y-%m-%d')

            # Setup an array to hold all messages.
            theMenu = []

            # Setup the request url for the canteens, ...
            canteensUrl = 'http://openmensa.org/api/v2' \
                + '/canteens?near[lat]=51.534535&near[lng]=9.933691' \
                + '&near[dist]=10'

            # ... fetch a list of canteens from openmensa.org ...
            canteensJson = urllib.request.urlopen(canteensUrl).read()

            # ... and generate a python list from json blob.
            canteens = json.loads(str(canteensJson, 'utf-8'))

            # Loop over all canteens and fetch their meals.
            for canteen in canteens:
                try:
                    # Add the canteen name to the message stack.
                    theMenu.append("{0}{1}{2}".format(Color.bold, canteen['name'], Color.clear))

                    # Setup the request url for the canteen, ...
                    mealsUrl = 'http://openmensa.org/api/v2' \
                        + '/canteens/' + str(canteen['id']) \
                        + '/days/' + today \
                        + '/meals'

                    # ... fetch a list of meals for this mensa ...
                    mealsJson = urllib.request.urlopen(mealsUrl).read()

                    # ... and generate a python list from json blob.
                    meals = json.loads(str(mealsJson, 'utf-8'))

                    # Loop over all meals and add them to the message stack.
                    for meal in meals:
                        theMenu.append("{0} - {1}€/{2}€/{3}€".format(meal['name'], meal['prices']['students'], meal['prices']['employees'], meal['prices']['others'] ))
                except urllib.error.HTTPError as e:
                    self.logger.info('No data for {}'.format(canteen['name'].encode()))
            # Finally send all messages to the irc channel.
            for entry in theMenu:
                self.send_message(entry, message.channel)
        except urllib.error.HTTPError as e:
            self.logger.info('Mensa service currently unavailable')
            self.send_message('[Mensa] Service currently unavailable', message.channel)
        except Exception:
            traceback.print_exc()
