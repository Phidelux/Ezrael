#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import socket
import random
import thread
import ssl
import os
from core.message import Message

COMMAND_PREFIX = "!"


# Defining a class to run the server. One per connection. This class will do most of our work.
class Ezrael(object):
    @staticmethod
    def map_strip(elements, to_lower=False):
        elements = map(lambda s: s.strip(), elements)
        if to_lower:
            elements = map(lambda s: s.lower(), elements)
        return elements

    @staticmethod
    def norm_channel(channel):
        if channel[0] == "#":
            return channel
        return "#" + channel

    command_prefix = COMMAND_PREFIX
    command_prefix_len = len(COMMAND_PREFIX)

    # The default constructor - declaring global variables
    # channel should be rewritten to be a list, which then loops to connect, per channel.
    # This needs to support an alternate nick.
    def __init__(self):
        # Fetch the current working directory ...
        base_path = os.path.dirname(os.path.realpath(__file__))
        base_path = base_path[:base_path.rfind('/')]

        # ... and generate the path to the config file.
        config_file = os.path.join(base_path, 'ezrael.ini')
        config_file_custom = os.path.join(base_path, 'ezrael.custom.ini')
        self.base_path = base_path

        # Load connection data from main config ...
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.config.read(config_file_custom)

        # ... and assign them to locals.
        self.ircHost = self.config['main']['host']
        self.ircPort = int(self.config['main']['port'])
        self.ircSSL = self.config['main']['ssl'].lower() in ['true', '1', 't']
        self.ircNick = self.config['main']['nick']
        self.ircPassword = self.config['main']['password']
        self.ircChannel = '#' + self.config['main']['channel']

        # TODO: Remove usage of debugging nickname.
        self.ircNick = "Ezrael{:0>2}".format(random.randint(1, 99))
        self.ircChannel = "#ezraeltest"

        # Setup the socket used to communicate with the irc, ...
        self.ircSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # ... initialize some class attributes ...
        self.isConnected = False
        self.pluginsLoaded = False
        self.shouldReconnect = False
        self.command = ''
        self.plugins = []

        self.admins = []
        if self.config['main']['plugins'] is not None:
            self.admins.extend(self.map_strip(self.config['main']['admins'].split(','), True))

        # ... and finally load all plugins enabled in the configuration.
        self.load_plugins()

    # This is the bit that controls connection to a server & channel.
    # It should be rewritten to allow multiple channels in a single server.
    # This needs to have an "auto identify" as part of its script, or support a custom connect message.
    def connect(self):
        self.shouldReconnect = True
        # noinspection PyBroadException
        try:
            self.ircSock.connect((self.ircHost, self.ircPort))
            if self.ircSSL:
                self.ircSock = ssl.wrap_socket(self.ircSock,
                                               # flag that certificate from the other side of connection is required
                                               # and should be validated when wrapping
                                               cert_reqs=ssl.CERT_REQUIRED,
                                               # file with root certificates
                                               ca_certs=os.path.join(self.base_path, "ca-certs.txt")
                                               )
        except:
            print("Error: Could not connect to Host " + str(self.ircHost) + ":" + str(self.ircPort))
            exit(1)  # TODO: We should make it reconnect if it gets an error here
        print("NOTICE: Connected to: " + str(self.ircHost) + ":" + str(self.ircPort))

        self.ircSock.send("NICK {0} \r\n".format(self.ircNick).encode())
        print("NOTICE: Setting bot nick to " + str(self.ircNick))

        self.ircSock.send("USER {0} 8 * :X\r\n".format(self.ircNick).encode())
        print("NOTICE: Setting User")

        self.ircSock.send("PRIVMSG nickserv :identify {0} {1}\r\n".format(self.ircNick, self.ircPassword).encode())
        print("******* Nickserv Identify")

        self.ircSock.send("JOIN {0} \r\n".format(self.ircChannel).encode())
        print("NOTICE: Joining channel " + str(self.ircChannel))

        self.ircSock.send("PRIVMSG chanserv :op {0} \r\n".format(self.ircChannel).encode())
        print("NOTICE: Trying to obtain operator status ...")

        self.isConnected = True
        self.listen()

    def load_plugins(self):
        if self.config['main']['plugins'] is not None:
            plugins = self.map_strip(self.config['main']['plugins'].split(','))

            for module in plugins:
                if module:
                    plugin = __import__('plugins.' + module.lower(), globals(), locals(), [module])
                    print('NOTICE: Loaded plugin ' + module)
                    instance = getattr(plugin, module)(self.config)
                    self.plugins.append(instance)

            self.notify_plugins('init')
            self.pluginsLoaded = True

    def fetch_admins(self):
        return self.admins

    def notify_plugins(self, event, *args):
        if not self.pluginsLoaded and event != 'init':
            return

        for plugin in self.plugins:
            getattr(plugin, event)(self, *args)

    def trigger(self, event, message):
        if message.propagate:
            self.notify_plugins(event, message)

    def listen(self):
        while self.isConnected:
            bunch = self.ircSock.recv(1024)
            if not bunch:
                continue
            try:
                msg = bunch.decode()
                msgs = msg.split("\r\n")
            except UnicodeDecodeError:
                msg = str(bunch)
                bounding = msg[1]
                msg = msg[2:len(msg) - 5].replace("\\" + bounding, bounding).replace("\\\\", "\\")
                msgs = msg.split("\\r\\n")
            # for each message within received bunch ...
            for m in msgs:
                if not m:
                    continue
                # ... generate Message-object, ...
                message = Message(self, m)
                print("Received %s" % str(message).encode('utf-8'))
                # ... run built-in commands and ...
                if len(message.cmd):
                    self.check_commands(message)
                # ... trigger events for plugins
                for event in message.get_events():
                    self.trigger(event, message)

        if self.shouldReconnect:
            self.connect()

    def check_commands(self, message):
        if message.nick.lower() in self.admins:
            # admin commands
            print("Command by {0}: {1}".format(message.nick, " ".join(message.cmd)))
            if message.cmd[0] == 'quit':
                self.ircSock.send("QUIT {0} \r\n".format(self.ircChannel).encode())
                self.ircSock.close()
                self.isConnected = False
                self.shouldReconnect = False

            elif message.cmd[0] == 'op':
                self.ircSock.send("MODE {0} +o {1} \r\n".format(message.channel, message.nick).encode())

            elif message.cmd[0] == 'join':
                if len(message.cmd) > 1:
                    for channel in message.cmd[1:]:
                        self.join_channel(self.norm_channel(channel))
                else:
                    self.send_message("Syntax: {0}join [#]CHANNEL,...".format(self.command_prefix), message.nick)

            elif message.cmd[0] == 'part' or message.cmd[0] == 'leave':
                if len(message.cmd) > 1:
                    for channel in message.cmd[1:]:
                        self.quit_channel(self.norm_channel(channel))
                else:
                    self.quit_channel(message.channel)

    def send(self, data):
        self.ircSock.send(data)

    def send_message(self, data, receiver):
        self.ircSock.send(("PRIVMSG %s :%s\r\n" % (receiver, data)).encode())

    def send_notice(self, data, receiver):
        self.ircSock.send(("NOTICE %s :%s\r\n" % (receiver, data)).encode())

    def join_channel(self, channel):
        channel = self.norm_channel(channel)
        self.ircSock.send("JOIN {0} \r\n".format(channel).encode())
        self.ircSock.send("PRIVMSG chanserv :op {0} \r\n".format(channel).encode())
        print("NOTICE: Trying to obtain operator status with Chanserv on %s" % channel)
        # This needs to test if the channel is full
        # This needs to modify the list of active channels

    def quit_channel(self, channel):
        channel = self.norm_channel(channel)
        self.ircSock.send("PART {0} \r\n".format(channel).encode())
        # This needs to modify the list of active channels
