from core.plugin import Plugin
import time

class LastSeen(Plugin):
    def init(self):
        # Initialize the list of users.
        self.last_seen = {}

    def update_lastseen(self, nick, channel):
        if nick not in self.last_seen.keys():
            self.last_seen[nick] = {}

        self.last_seen[nick][channel] = time.strftime("%a, %d. %b %Y - %H:%M")

    def on_join(self, message):
        self.update_lastseen(message.nick, message.channel)

    def on_quit(self, message):
        self.update_lastseen(message.nick, message.channel)

    def on_message(self, message):
        self.update_lastseen(message.nick, message.channel)
        
    def on_command(self, message):
        # Check if topic change request was sent.
        if message.cmd[0] != 'lastseen':
            return

        # Split the message in command and username ...
        words = message.content.split()

        # ...and extract the nickname from the command.
        nickname = words[1].strip() if len(words) >= 2 else None

        if nickname == self.context['nick']:
            self.send_message("I am currently running, dumbass!", message.channel)
        elif nickname in self.last_seen.keys() and message.channel in self.last_seen[nickname].keys():
            self.send_message(
                  "Last time I saw {0} was {1}.".format(
                        nickname, self.last_seen[nickname][message.channel]), 
                  message.channel)
        else:
            self.send_message("Didn't see {0} for a long time.".format(nickname),
                  message.channel)
