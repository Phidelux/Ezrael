from core.plugin import Plugin
import time

class Topic(Plugin):
    def init(self):
        # Initialize update timer and threshold.
        self.last_update = 0
        self.threshold = 30

        if 'topic_update_threshold' in self.context:
            self.threshold = self.context['topic_update_threshold']

    def on_command(self, message):
        # Check if topic change request was sent.
        if message.cmd[0] != 'topic':
            return

        # Check if topic could be changed again.
        if time.time() - self.last_update > self.threshold:
            # Update the topic update timer, ...
            self.last_update = time.time()

            # ... extract the new topic text from the command ...
            msg = message.content[self.context['command_prefix_len'] + len(message.cmd[0]):].strip()

            # ... and set the topic.
            self.send("TOPIC {} :{}\n".format(message.channel, msg).encode())
