#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.colors import Color
import socket, time
import configparser
import random
import os
import ssl

# Defining a class to run the server. One per connection. This class will do most of our work.
class Ezrael(object):
   # The default constructor - declaring global variables
   # channel should be rewritten to be a list, which then loops to connect, per channel.
   # This needs to support an alternate nick.
   def __init__(self):
      # Fetch the current working directory ...
      basepath = os.path.dirname(os.path.realpath(__file__))
      basepath = basepath[:basepath.rfind('/')]

      # ... and generate the path to the config file.
      configFile = os.path.join(basepath, 'ezrael.ini')
      configFileCustom = os.path.join(basepath, 'ezrael.custom.ini')
      self.caCertsPath = os.path.join(basepath, "cacerts.txt")

      # Load connection data from main config ...
      self.config = configparser.ConfigParser()
      self.config.read(configFile)
      self.config.read(configFileCustom)

      # ... and assign them to locals.
      self.ircHost = self.config['main']['host']
      self.ircPort = int(self.config['main']['port'])
      self.ircSSL = self.config['main']['ssl'].lower() in ['true', '1', 't']
      self.ircNick = self.config['main']['nick']
      self.ircPassword = self.config['main']['password']
      self.ircChannel = '#' + self.config['main']['channel']

      # TODO: Remove usage of debugging nickname.
      self.ircNick = "Ezrael{:0>2}".format(random.randint(1, 99))

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
         self.admins.extend(self.parseParameterList(self.config['main']['admins'], ',', True))

      # ... and finally load all plugins enabled in the configuration.
      self.loadPlugins()

   # This is the bit that controls connection to a server & channel.
   # It should be rewritten to allow multiple channels in a single server.
   # This needs to have an "auto identify" as part of its script, or support a custom connect message.
   def connect(self):
      self.shouldReconnect = True
      try:
         self.ircSock.connect((self.ircHost, self.ircPort))
         if self.ircSSL:
            self.ircSock = ssl.wrap_socket(self.ircSock,
                                           # flag that certificate from the other side of connection is required
                                           # and should be validated when wrapping
                                           cert_reqs=ssl.CERT_REQUIRED,
                                           # file with root certificates
                                           ca_certs=self.caCertsPath
                                           )
      except:
         print("Error: Could not connect to Host " + str(self.ircHost) + ":" + str(self.ircPort))
         exit(1) # TODO: We should make it reconnect if it gets an error here
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
      print("NOTICE: Trying to optain operator status ...")

      self.isConnected = True
      self.listen()

   def loadPlugins(self):
      if self.config['main']['plugins'] is not None:
         plugins = self.parseParameterList(self.config['main']['plugins'], ',')

         for module in plugins:
            plugin = __import__('plugins.' + module.lower(), globals(), locals(), [module])
            print('NOTICE: Loaded plugin ' + module)
            instance = getattr(plugin, module)(self.config)
            self.plugins.append(instance)

         self.notifyPlugins('init')
         self.pluginsLoaded = True

   def fetchAdmins(self):
      return self.admins

   def parseParameterList(self, data, seperator, toLower = False):
      # Split data into element list ...
      elemList = data.split(seperator)

      # ... and strip leading and trailing spaces from each element.
      elemList = map(lambda s: s.strip(), elemList)

      # If needed convert all elements to lower.
      if toLower == True:
         elemList = map(lambda s: s.lower(), elemList)

      return elemList

   def notifyPlugins(self, event, *args):
      if not self.pluginsLoaded and event != 'init':
         return

      for plugin in self.plugins:
         getattr(plugin, event)(self, *args)

   def listen(self):
      while self.isConnected:
         recv = self.ircSock.recv(1024)

         if recv != "":
            print(str(recv))

            # Notify the plugins that we received something.
            ircUserMessage = self.extractMessage(recv)
            self.notifyPlugins('onRecv', ircUserMessage)

            # Notify the plugins if we received a private message.
            if str(recv).find("PRIVMSG " + self.ircNick) != -1:
               ircUserNick = self.extractUser(recv)
               ircUserHost = self.extractHost(recv)
               self.notifyPlugins('onPrivMsg', self.ircChannel, ircUserNick, ircUserMessage)

            # Notify the plugins if we received a message.
            elif str(recv).find("PRIVMSG") != -1:
               ircUserNick = self.extractUser(recv)
               ircUserHost = self.extractHost(recv)
               self.notifyPlugins('onMsg', self.ircChannel, ircUserNick, ircUserMessage)

               # Print normal messages.
               print ( (str(recv)).split()[2]  + "@" + ircUserNick + ": " + ircUserMessage)

               # "!" Indicated a command
               if len(str(ircUserMessage)) > 0 and str(ircUserMessage[0]) == "!":
                  self.command = ircUserMessage
                  self.processCommand(ircUserNick, self.ircChannel)
               else:
                  self.processMessage(ircUserMessage, ircUserNick, self.extractMessage(recv) )

            # Notify the plugins if we were kicked from the channel.
            elif str(recv).find("KICK " + self.ircChannel + " " + self.ircNick) != -1:
               ircUserNick = self.extractUser(recv)
               self.notifyPlugins('onKick', self.ircChannel, ircUserNick, ircUserMessage)

            # Notify the plugins if someone joined the channel.
            elif str(recv).find("JOIN " + self.ircChannel ) != -1:
               ircUserNick = self.extractUser(recv)
               self.notifyPlugins('onJoin', self.ircChannel, ircUserNick, ircUserMessage)

               # Send a greet to users joining the channel.
               if(ircUserNick != self.ircNick):
                  self.ircSock.send("NOTICE {0} :Welcome to {1}. \r\n".format(ircUserNick, self.ircChannel).encode())

            # Notify the plugins if someone pinged ezrael.
            elif str(recv).find("PING") != -1:
               self.notifyPlugins('onPing', ircUserMessage)

               # Send a PONG on an incoming PING.
               print("NOTICE: PONG {0}\r\n".format(recv.split()[1]).encode())
               self.ircSock.send("PONG {0}\r\n".format(recv.split()[1]).encode() )

            # Notify the plugins if someone writes a notice.
            elif str(recv).find("NOTICE") != -1:
               ircUserNick = self.extractUser(recv)
               self.notifyPlugins('onNotice', self.ircChannel, ircUserNick, ircUserMessage)

      if self.shouldReconnect:
         self.connect()

   def extractUser(self, recv):
      return str(recv).split('!')[0].split(':')[1]

   def extractHost(self, recv):
      return str(recv).split('@')[1].split(' ')[0]

   def extractMessage(self, recv):
      return self.data2message(str(recv))

   def data2message(self,data):
      # Remove leading colon ...
      data = data[data.find(':')+1:len(data)]

      # ... and extract all data after the next one.
      data = data[data.find(':')+1:len(data)]

      # Remove strange data at end of line.
      if data[len(data)-5:] == "\\r\\n'":
         data = data[0:len(data)-5]

      return data.strip()

   def processMessage(self, data, nickname, channel):
      # TODO: Implement Plugin based message handling.
      pass

   def sendPlain(self, data):
      self.ircSock.send(data)

   def sendMessage2Nick(self, data, nick):
      self.ircSock.send( (("PRIVMSG %s :%s\r\n") % (nick, data)).encode() )

   # This function sends a message to a channel, which must start with a #.
   def sendMessage2Channel(self, data, channel):
      print( "{0}: {1}".format(self.ircNick, data) )
      self.ircSock.send( (("PRIVMSG %s :%s\r\n") % (channel, data)).encode() )

   # This function takes a channel, which must start with a #.
   def joinChannel(self, channel):
      if (channel[0] == "#"):
         self.ircSock.send ("JOIN {0} \r\n".format(channel).encode())
         self.ircSock.send ("PRIVMSG chanserv :op {0} \r\n".format(channel).encode())
         print ("NOTICE: Trying to obtain operator status with Chanserv on %s" % channel)

         # This needs to test if the channel is full
         # This needs to modify the list of active channels

   # This function takes a channel, which must start with a #.
   def quitChannel(self,channel):
      if (channel[0] == "#"):
         self.ircSock.send ("PART {0} \r\n".format(channel).encode())
         # This needs to modify the list of active channels

   # This nice function here runs ALL the commands.
   # For now, we only have 2: root admin, and anyone.
   def processCommand(self, user, channel):
      # This line makes sure an actual command was sent, not a plain "!"
      if ( len(self.command.split()) == 0):
         return

      command = self.command[1:].split()[0].strip().lower()
      data = self.command[1+len(command):].strip()

      print("User: {0}".format(user))
      print("Channel: {0}".format(channel))
      print("Command: {0}".format(command))
      print("Data: {0}".format(data))

      # All admin only commands go in here.
      if (user.lower() in self.admins):
         # This command shuts the bot down.
         if (command == "quit"):
            self.ircSock.send("QUIT {0} \r\n".format(channel).encode())
            self.ircSock.close()
            self.isConnected = False
            self.shouldReconnect = False

         elif (command == "op"):
            self.ircSock.send("MODE {0} +o Avedo \r\n".format(channel).encode())
            self.sendMessage2Channel("It wants op from me", channel )

         # These commands take parameters
         else:
            # This command makes the bot join a channel
            # This needs to be rewritten in a better way, to catch multiple channels
            if (command == "join"):
               if ( data[0] == "#"):
                  irc_channel = data.split()[0]
               else:
                  irc_channel = "#" + data.split()[0]
               self.joinChannel(irc_channel)

            # This command makes the bot part a channel
            # This needs to be rewritten in a better way, to catch multiple channels
            if (command[0] == "part"):
               if ( data[0] == "#"):
                  irc_channel = data.split()[0]
               else:
                  irc_channel = "#" + data.split()[0]

               self.quitChannel(irc_channel)