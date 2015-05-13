#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.colors import Color
import socket, time
import configparser
import random
import os

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

      # Load connection data from main config ...
      self.config = configparser.ConfigParser()
      self.config.read(configFile)

      # ... and assign them to locals.
      self.ircHost = self.config['main']['host']
      self.ircPort = int(self.config['main']['port'])
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

      # ... and finally load all plugins enabled in the configuration.
      self.loadPlugins()

   # This is the bit that controls connection to a server & channel.
   # It should be rewritten to allow multiple channels in a single server.
   # This needs to have an "auto identify" as part of its script, or support a custom connect message.
   def connect(self):
      self.shouldReconnect = True
      try:
         self.ircSock.connect((self.ircHost, self.ircPort))
      except:
         print("Error: Could not connect to Host " + str(self.ircHost) + ":" + str(self.ircPort))
         exit(1) # TODO: We should make it reconnect if it gets an error here
      print("******* Connected to: " + str(self.ircHost) + ":" + str(self.ircPort))

      buffer = ("NICK %s \r\n" % self.ircNick)
      self.ircSock.send(buffer.encode())
      print("******* Setting bot nick to " + str(self.ircNick))

      buffer = ("USER %s 8 * :X\r\n" % self.ircNick)
      self.ircSock.send(buffer.encode())
      print("******* Setting User")

      # TODO: Reactivate for bot login.
      # buffer = ("PRIVMSG nickserv :identify %s %s\r\n" % (self.ircNick, self.ircPassword))
      # self.ircSock.send(buffer.encode())
      # print("******* Nickserv Identify")

      buffer = ("JOIN %s \r\n"  % self.ircChannel)
      self.ircSock.send(buffer.encode())
      print("******* Joining channel " + str(self.ircChannel))

      buffer = ("PRIVMSG chanserv :op %s \r\n" % self.ircChannel)
      self.ircSock.send (buffer.encode())
      print("******* try to op me")

      self.isConnected = True
      self.listen()

   def loadPlugins(self):
      if self.config['main']['plugins'] is not None:
         plugins = self.config['main']['plugins'].split(',')

         for module in plugins:
            plugin = __import__('plugins.' + module.lower(), globals(), locals(), [module])
            print('Loaded plugin ' + module)
            instance = getattr(plugin, module)(self.config)
            self.plugins.append(instance)

         self.notifyPlugins('init')
         self.pluginsLoaded = True

   def notifyPlugins(self, event, *args):
      if not self.pluginsLoaded and event != 'init':
         return

      for plugin in self.plugins:
         getattr(plugin, event)(self, *args)

   def listen(self):
      while self.isConnected:
         recv = self.ircSock.recv(1024)

         if recv != "":
            # TODO: Debugging output.
            print('Received: ' + str(recv))

            # Notify the plugins that we received something.
            ircUserMessage = self.extractMessage(recv)
            self.notifyPlugins('onRecv', ircUserMessage)

            # Notify the plugins if we received a private message.
            if str(recv).find("PRIVMSG " + self.ircNick) != -1:
               ircUserNick = self.extractUser(recv)
               self.notifyPlugins('onPrivMsg', self.ircChannel, ircUserNick, ircUserMessage)

            # Notify the plugins if we received a message.
            elif str(recv).find("PRIVMSG") != -1:
               ircUserNick = self.extractUser(recv)
               self.notifyPlugins('onMsg', self.ircChannel, ircUserNick, ircUserMessage)

            # Notify the plugins if we were kicked from the channel.
            elif str(recv).find("KICK " + self.ircChannel + " " + self.ircNick) != -1:
               ircUserNick = self.extractUser(recv)
               self.notifyPlugins('onKick', self.ircChannel, ircUserNick, ircUserMessage)

            if str(recv).find("PING") != -1:
               print("Sent: PONG ".encode() + recv.split()[1] + "\r\n".encode())
               self.ircSock.send("PONG ".encode() + recv.split()[1] + "\r\n".encode() )

            # TODO: Welcome message works.
            if str(recv).find("JOIN " + self.ircChannel ) != -1:
               ircUserNick = self.extractUser(recv)
               # if the bot joins a channel do nothing
               if(ircUserNick != self.ircNick):
                  buffer = ("NOTICE %s :Willkommen im " + self.ircChannel + " Channel. \r\n") % ircUserNick
                  self.ircSock.send(buffer.encode())

            if str(recv).find("NOTICE") != -1:
               ircUserNick = self.extractUser(recv)
               ircUserMessage = self.extractMessage(recv)
               print ( "Notice! " + ircUserNick + "->" + ircUserMessage + "\r\n" )

            if str(recv).find ( "PRIVMSG " + self.ircNick ) != -1:
               ircUserNick = self.extractUser(recv)
               ircUserHost = self.extractHost(recv)
               ircUserMessage = self.extractMessage(recv)
               print ( "Query "  + "@" + ircUserNick + ": " + ircUserMessage)
               self.privCommand(ircUserNick, ircUserMessage )

            elif str(recv).find ( "PRIVMSG" ) != -1:
               ircUserNick = self.extractUser(recv)
               ircUserHost = self.extractHost(recv)
               ircUserMessage = self.extractMessage(recv)
               print ( (str(recv)).split()[2]  + "@" + ircUserNick + ": " + ircUserMessage)

               # "!" Indicated a command
               if ( str(ircUserMessage[0]) == "!" ):
                  self.command = ircUserMessage
                  self.processCommand(ircUserNick, ircUserMessage)
               else:
                  self.processMessage(ircUserMessage, ircUserNick, self.extractMessage(recv) )

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

   def privCommand(self, user, data):
      command = (data).lower()
      command = command.split()
      print(command)
      if (command[0] == "join"):
         print ("er will joinen")
         self.joinChannel(command[1])

         str_buff = ("NOTICE " + user + " :Joined Channel " + command[1] + "\r\n")
         self.ircSock.send(str_buff.encode())

   def processMessage(self, data, nickname, channel):
      # TODO: Implement Plugin based message handling.
      pass

   def sendPlain(self, data):
      self.ircSock.send(data)

   # This function sends a message to a channel, which must start with a #.
   def sendMessage2Channel(self,data,channel):
      print ( ( "%s: %s") % (self.ircNick, data) )
      self.ircSock.send( (("PRIVMSG %s :%s\r\n") % (channel, data)).encode() )

   # This function takes a channel, which must start with a #.
   def joinChannel(self,channel):
      if (channel[0] == "#"):
         str_buff = ( "JOIN %s \r\n" ) % (channel)
         self.ircSock.send (str_buff.encode())
         buffer = ("PRIVMSG chanserv :op %s \r\n") % (channel)
         self.ircSock.send (buffer.encode())
         print ("******* Try to OP me with Chanserv on %s" % channel)

         # This needs to test if the channel is full
         # This needs to modify the list of active channels

   # This function takes a channel, which must start with a #.
   def quitChannel(self,channel):
      if (channel[0] == "#"):
         str_buff = ( "PART %s \r\n" ) % (channel)
         self.ircSock.send (str_buff.encode())
         # This needs to modify the list of active channels

   # This nice function here runs ALL the commands.
   # For now, we only have 2: root admin, and anyone.
   def processCommand(self, user, channel):
      # This line makes sure an actual command was sent, not a plain "!"
      if ( len(self.command.split()) == 0):
         return

      command = self.command[1:].split()[0].strip().lower()
      data = self.command[1+len(command):].strip()

      print("User: " + user)
      print("Command: " + command)
      print("Data: " + data)

      # All admin only commands go in here.
      if (user == "Avedo"):
         # This command shuts the bot down.
         if (command == "quit"):
            str_buff = ( "QUIT %s \r\n" ) % (channel)
            self.ircSock.send (str_buff.encode())
            self.ircSock.close()
            self.isConnected = False
            self.shouldReconnect = False

         elif (command == "op"):
            str_buff = ("MODE %s +o Avedo \r\n") % (channel)
            self.ircSock.send (str_buff.encode())
            self.sendMessage2Channel( ("4Es will op von mir"), channel )

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