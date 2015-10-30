__author__ = 'frissdiegurke'

# TODO: Use the new messaging interface.

import os
import json

from core.plugin import Plugin

VERSION = 0


class Echo:
    message = None

    def __init__(self):
        self.message = []

    def add_line(self, msg):
        self.message.append(msg)

    def revert(self, amount):
        for i in range(1, amount):
            self.message.pop()

class Record(Plugin):
    registry = {"__v": VERSION}
    current = {}
    registry_file = ""

    def init(self, message):
        self.registry_file = os.path.join(irc.base_path, "plugins/data/record-registry.json")
        try:
            with open(self.registry_file, 'r') as f:
                reg = json.load(f)
                if reg["__v"] == VERSION:
                    self.registry = reg
                elif reg["__v"] < VERSION:
                    print("Record-Plugin: Config version conflict detected.")
        except FileNotFoundError:
            pass

    def attempt_save(self, echo, channel, nick, name, overwrite):
        if not overwrite and name in self.registry:
            self.send_message("Record already existing. Use !overwrite instead.", nick)
        else:
            self.registry[name] = echo.message
            del self.current[channel][nick]

    def on_message(self, message):
        name = message.content[1:].lower()

        if len(message.content) and message.content[0] == "$" and name in self.registry:
            for l in self.registry[name]:
                self.send_message(l, message.channel)
            return

        # only admins are allowed to define/change records
        if message.nick.lower() not in irc.admins:
            return

        if len(message.cmd):

            if message.cmd[0] == "record":
                if message.channel not in self.current:
                    self.current[message.channel] = {}
                self.current[message.channel][message.nick] = Echo()
                return

            if message.cmd[0] == "persist":
                try:
                    with open(self.registry_file, 'w') as f:
                        json.dump(self.registry, f)
                except FileNotFoundError:
                    os.makedirs(os.path.dirname(self.registry_file))
                    with open(self.registry_file, 'w') as f:
                        json.dump(self.registry, f)
                except PermissionError:
                    print("NOTICE: No permission to persist records.")
                    self.send_message("Filesystem permission error while attempting to store records.", message.nick)
                return

            if message.cmd[0] == 'erase' and len(message.cmd) > 1:
                del self.registry[message.cmd[1].lower()]
                return

        # stop here if not recording
        if message.channel not in self.current or message.nick not in self.current[message.channel]:
            return

        echo = self.current[message.channel][message.nick]

        if len(message.cmd):
            if message.cmd[0] == 'stop':
                del self.current[message.channel][message.nick]
            elif message.cmd[0] == 'ignore':
                pass
            elif len(message.cmd) > 1:
                if message.cmd[0] == 'revert':
                    echo.revert(int(message.cmd[1]) or 1)
                elif message.cmd[0] == 'save':
                    self.attempt_save(echo, message.channel, message.nick, message.cmd[1].lower(), False)
                elif message.cmd[0] == 'overwrite':
                    self.attempt_save(echo, message.channel, message.nick, message.cmd[1].lower(), True)
                else:
                    echo.add_line(message.content)
            else:
                echo.add_line(message.content)
        else:
            echo.add_line(message.content)
