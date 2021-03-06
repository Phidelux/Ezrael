#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.message import Message
from core.msghandler import MessageHandler
from core.utils import decode

import configparser
import logging
import socket
import random
import _thread
import time
import ssl
import os

COMMAND_PREFIX = "!"

def decode(bytes):
    try: 
        text = bytes.decode('utf-8')
    except UnicodeDecodeError: 
        try: 
            text = bytes.decode('iso-8859-1')
        except UnicodeDecodeError: 
            text = bytes.decode('cp1252')
    
    return text

# Defining a class to run the server. One per connection. This class will do most of our work.
class Ezrael(MessageHandler):
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
    def __init__(self, debugging):
        # Fetch an instance of the logger.
        if debugging:
            self.logger = logging.getLogger('development')
        else:
            self.logger = logging.getLogger('production')

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

        if debugging ==  True:
            self.ircNick = "Ezrael{:0>2}".format(random.randint(1, 99))
            self.ircChannel = "#ezraeltest"

        # Set the correct timezone.
        if self.config['main']['timezone'] is not None:
            self.timezone = self.config['main']['timezone'].strip()
            os.environ['TZ'] = self.timezone
            time.tzset()

        # Setup the socket used to communicate with the irc, ...
        self.ircSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # ... initialize some class attributes, ...
        self.isConnected = False
        self.pluginsLoaded = False
        self.shouldReconnect = self.config['main']['reconnect'].lower() in ['true', '1', 't']
        self.reconnectDelay = int(self.config['main']['reconnect_delay'])
        self.command = ''
        self.plugins = []

        self.admins = []
        if self.config['main']['plugins'] is not None:
            self.admins.extend(self.map_strip(self.config['main']['admins'].split(','), True))
        
        # ... build an application context for the plugins ...
        self.context = {
            'host': self.ircHost,
            'port': self.ircPort,
            'nick': self.ircNick,
            'admins': self.admins,
            'timezone': self.timezone,
            'base_path': self.base_path,
            'debugging': debugging,
            'command_prefix': self.command_prefix,
            'command_prefix_len': self.command_prefix_len
        }

        # ... and finally load all plugins enabled in the configuration.
        self.load_plugins()

    # This is the bit that controls connection to a server & channel.
    # It should be rewritten to allow multiple channels in a single server.
    # This needs to have an "auto identify" as part of its script, or support a custom connect message.
    def connect(self):
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

            self.logger.info("Connected to: " + str(self.ircHost) + ":" + str(self.ircPort))

            self.send("NICK {0} \r\n".format(self.ircNick).encode())
            self.logger.info("Setting bot nick to " + str(self.ircNick))

            self.send("USER {0} 8 * :X\r\n".format(self.ircNick).encode())
            self.logger.info("Setting User")

            self.send("PRIVMSG nickserv :identify {0} {1}\r\n".format(self.ircNick, self.ircPassword).encode())
            self.logger.info("******* Nickserv Identify")

            self.send("JOIN {0} \r\n".format(self.ircChannel).encode())
            self.logger.info("Joining channel " + str(self.ircChannel))

            self.send("PRIVMSG chanserv :op {0} \r\n".format(self.ircChannel).encode())
            self.logger.info("Trying to obtain operator status ...")

            self.isConnected = True
            self.listen()
        except:
            self.logger.error("Could not connect to Host " + str(self.ircHost) + ":" + str(self.ircPort))
            
            if self.shouldReconnect:
                time.sleep(self.reconnectDelay)
                self.connect()
        
    def load_plugins(self):
        if self.config['main']['plugins'] is not None:
            plugins = self.map_strip(self.config['main']['plugins'].split(','))

            for module in plugins:
                if module:
                    plugin = __import__('plugins.' + module.lower(), globals(), locals(), [module])
                    self.logger.info('Loaded plugin ' + module)
                    instance = getattr(plugin, module)(self.context)
                    self.plugins.append(instance)
                    _thread.start_new_thread(self.pluginHandling, (instance, ))

            self.notify_plugins('init')
            self.pluginsLoaded = True

    def notify_plugins(self, event, *args, **kwargs):
        if not self.pluginsLoaded and event != 'init':
            return

        for plugin in self.plugins:
            plugin.queue(event, *args, **kwargs)

    def trigger(self, event, message):
        if message.propagate:
            self.notify_plugins(event, message)

    def listen(self):
        while self.isConnected:
            bunch = self.ircSock.recv(4096)
            if not bunch:
                continue
            try:
                msg = decode(bunch)
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
                self.logger.info("Received %s" % str(message))
                # ... run built-in commands and ...
                if len(message.cmd):
                    self.check_commands(message)
                # ... trigger events for plugins
                for event in message.get_events():
                    self.trigger(event, message)

        if self.shouldReconnect:
            self.connect()

    def pluginHandling(self, plugin):
        sent = 0
        lastsent = time.time()

        while True:
            send = plugin.queue_out.get()

            if time.time() - lastsent > 10:
                sent = 0

            self.logger.info("-> '{}'".format(decode(send)))
            self.send(send)
            lastsent = time.time()
            sent += 1

            if sent >= 5:
                time.sleep(1)

    def check_commands(self, message):
        if message.nick.lower() in self.admins:
            # admin commands
            self.logger.info("Command by {0}: {1}".format(message.nick, " ".join(message.cmd)))
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
