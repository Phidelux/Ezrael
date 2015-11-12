from core.plugin import Plugin
from collections import namedtuple
import time

# Define a Note struct.
Note = namedtuple("Note", "time sender message")

class Notes(Plugin):
    def init(self):
        # Initialize the message stack.
        self.notes = {}

    def save(self, note):
        if nick not in self.notes.keys():
            self.notes[nick] = []

        self.notes[nick].append(note)

    def clear(self, nick):
        if nick in self.notes.keys():
            self.notes[nick] = []

    def on_command(self, message):
        if message.cmd[0] not in ['note', 'mynotes']:
            return

        if message.cmd[0] == 'mynotes' and message.nick in self.notes.keys():
            for note in self.notes[message.nick]:
                self.send_message("{0}: {1} | {2}".format(
                        note.time, note.sender, note.message))

            self.clear(message.nick)
        elif message.cmd[0] == 'note':
            pass
