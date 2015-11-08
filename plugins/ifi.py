from core.plugin import Plugin
from core.colors import Color
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import datetime

class Ifi(Plugin):
    def init(self):
        # Initialize update timer and threshold.
        self.last_update = 0
        self.threshold = 30

        if 'ifi_threshold' in self.context:
            self.threshold = self.context['ifi_threshold']

    def on_command(self, message):
        if message.cmd[0] != 'ifi':
            return

        # Check if ifi could be executed again.
        if time.time() - self.last_update > self.threshold:
            # Update the topic update timer, ...
            self.last_update = time.time()

            try:    
                # Setup the request url ...
                ifiUrl = 'http://display.informatik.uni-goettingen.de/events.html'

                # ... and fetch the list of currently running lectures.
                htmlBlob = urllib.request.urlopen(ifiUrl).read()

                # Initialize BeautifulSoup, ...
                soup = BeautifulSoup(resultBlob, "html5lib")

                # ... find the container of the lecture list ...
                container = soup.find(id="id_content")

                # ... and extract the list.
                lectureList = container.find("table").tbody.find_all("tr")

                # Loop over all lectures.
                for lecture in lectureList:
                    # Fetch all cells ...
                    cells = lecture.find_all("<td>")

                    # ... and check if there are running lectures.
                    if len(cells) == 1:
                        self.send_message(cells[0].get_text(), message.channel)
                        break

                    # Setup the message ...
                    lectureDesc = "{0} {1}{2}{3} | {4}".format(
                          cells[0], Color.bold, cells[1], Color.clear, cells[3])

                    # ... and send it.
                    self.send_message(lectureDesc, message.channel)
            except urllib.error.HTTPError as e:
                self.send_message('[Mensa] Service currently unavailable', message.channel)
