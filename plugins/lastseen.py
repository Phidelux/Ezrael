from core.plugin import Plugin
import datetime

class LastSeen(Plugin):
    def init(self):
        # Initialize the list of users.
        self.last_seen = {}

    def update_lastseen(self, username):
        now = datetime.datetime.now()
        self.last_seen[username] = now.strftime("%A, %d. %B %Y - %H:%M")

    def on_join(self, message):
        self.update_lastseen(message.nick)

    def on_message(self, message):
        self.update_lastseen(message.nick)
        
    def on_command(self, message):
        # Check if topic change request was sent.
        if message.cmd[0] != 'lastseen':
            return

        # Split the message in command and username ...
        words = message.content.split()

        # ...and extract the username from the command.
        username = words[1].strip() if len(words) >= 2 else None

        if username == self.context['nick']:
            self.send_message("I am currently running, dumbass!", message.channel)
        elif username in self.last_seen.keys():
            self.send_message(
                  "Last time I saw {0} was {1}.".format(
                        username, self.last_seen[username]), 
                  message.channel)
        else:
            self.send_message("Did not see {0} for a long time.".format(username),
                  message.channel)
