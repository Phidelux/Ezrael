from core.plugin import Plugin
from collections import namedtuple
import time

# Define a Note struct.
Note = namedtuple("Note", "timestamp sender message")

class Notes(Plugin):
    def init(self):
        # Initialize the message stack.
        self.notes = {}

    def save(self, nick, note):
        if nick not in self.notes.keys():
            self.notes[nick] = []

        self.notes[nick].append(note)

    def clear(self, nick):
        if nick in self.notes.keys():
            del self.notes[nick]

    def on_command(self, message):
        if message.cmd[0] not in ['note', 'mynotes']:
            return

        if message.cmd[0] == 'mynotes':
            if message.nick in self.notes.keys():
                for note in self.notes[message.nick]:
                    self.send_message("{0}: {1} | {2}".format(
                          note.timestamp, note.sender, note.message), message.channel)

                self.clear(message.nick)
            else:
                self.send_message('No notes for you!', message.channel)
        elif message.cmd[0] == 'note':
            # Split the message in command, username and message ...
            words = message.content.split()

            # ... and check if a nickname and message were given.
            if len(words) < 3:
                return

            # Fetch the given nickname, ...
            nickname = words[1].strip()

            # ... extract the message, ...
            msgText = ' '.join(words[2:])

            # ... fetch the current timestamp ...
            timestamp = time.strftime("%d. %b %Y, %H:%M")

            print("{0}: {1} -> {2} | {3}".format(timestamp, message.nick, nickname, msgText))

            # ... and save the new note.
            self.save(nickname, Note(timestamp, message.nick, msgText))
