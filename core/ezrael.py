#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.colors import Color
import socket, time
import configparser
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

      buffer = ("PRIVMSG nickserv :identify %s %s\r\n" % (self.ircNick, self.ircPassword))
      self.ircSock.send(buffer.encode())
      print("******* Nickserv Identify")

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
                  self.command = str(ircUserMessage[1:])
                  # (str(recv)).split()[2] ) is simply the channel the command was heard on.
                  self.processCommand(ircUserNick, ( (str(recv)).split()[2] ) )
               else:
                  self.processMessage(ircUserMessage, ircUserNick, ( (str(recv)).split()[2] ) )

            #KickProtection for Ezrael when anybody kicks him he rejoins deop's and kick's the user
            if str(recv).find ( "KICK "+self.ircChannel+" Ezrael" ) != -1:
               ircKickUserNick = str(recv).split ( '!' )[0].split(":")[1]
               print ('******* !!! - I was kicked by ' + ircKickUserNick + ' from ' + self.ircChannel + '\r\n')
               self.joinChannel(self.ircChannel)
               print ('******* Rejoining ...'+self.ircChannel)
               time.sleep(1)
               str_buff = ("MODE %s -o " + ircKickUserNick + " \r\n") % (self.ircChannel)
               self.ircSock.send (str_buff.encode())
               str_buff = ("KICK %s " + ircKickUserNick + " :Kick yourself!\r\n") % (self.ircChannel)
               self.ircSock.send (str_buff.encode())

      if self.shouldReconnect:
         self.connect()

   def extractUser(self, recv):
      return str(recv).split('!')[0].split(':')[1]

   def extractHost(self, recv):
      return str(recv).split('@')[1].split(' ')[0]

   def extractMessage(self, recv):
      return self.data2message(str(recv))

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
      # if (nickname == "Avedo" and data == "hallo"):
      #    self.sendMessage2Channel( ("Hallo Gott"), channel )
      # elif (data == "hallo"):
      #    self.sendMessage2Channel( ("Hallo, " + nickname), channel )
      # elif (data == "HaLl0" or data == "hall0" or data == "ha110"):
      #    self.sendMessage2Channel( ("\x01ACTION slaps " + nickname + "around a bit with a large dick\x01"), channel )
      # elif (data == "fu" or data == "FU"):
      #    self.sendMessage2Channel( ("fu dich selber du bengel"), channel )
      # elif (data == "slaps Ezrael"):
      #    self.sendMessage2Channel( ("slap dich selber du schuettelwurm!"), channel )
      # elif (data == "duck"):
      #    self.sendMessage2Channel( ('__("<'), channel )
      #    self.sendMessage2Channel( ('\__/'), channel )
      #    self.sendMessage2Channel( (' ^^'), channel )
      #    self.sendMessage2Channel( ("DUCKTALES DADADAAAAAA"), channel )

   def data2message(self,data):
      data = data[data.find(':')+1:len(data)]
      data = data[data.find(':')+1:len(data)]
      data = str(data[0:len(data)-5])
      return data

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

      # So the command isn't case sensitive
      command = (self.command).lower()

      # Break the command into pieces, so we can interpret it with arguments
      command = command.split()

      # All admin only commands go in here.
      if (user == "Avedo"):
         if ( len(command) == 1):
            # This command shuts the bot down.
            if (command[0] == "quit"):
               str_buff = ( "QUIT %s \r\n" ) % (channel)
               self.ircSock.send (str_buff.encode())
               self.ircSock.close()
               self.isConnected = False
               self.shouldReconnect = False

            elif (command[0] == "op"):
               str_buff = ("MODE %s +o Avedo \r\n") % (channel)
               self.ircSock.send (str_buff.encode())
               self.sendMessage2Channel( ("4Es will op von mir"), channel )

         # These commands take parameters
         else:
            # This command makes the bot join a channel
            # This needs to be rewritten in a better way, to catch multiple channels
            if (command[0] == "join"):
               if ( (command[1])[0] == "#"):
                  irc_channel = command[1]
               else:
                  irc_channel = "#" + command[1]
               self.joinChannel(irc_channel)

            # This command makes the bot part a channel
            # This needs to be rewritten in a better way, to catch multiple channels
            if (command[0] == "part"):
               if ( (command[1])[0] == "#"):
                  irc_channel = command[1]
               else:
                  irc_channel = "#" + command[1]
                  self.quitChannel(irc_channel)

      # All public commands go here
      # The first set of commands are ones that don't take parameters
      if ( len(command) == 1):
         if (command[0] == "test"):
            self.sendMessage2Channel( ('\033[0;31mtest'), channel )
         if (command[0] == "moo"):
            self.sendMessage2Channel( ("MOO yourself, " + user), channel )
         if (command[0] == "train"):
            self.sendMessage2Channel( ("Choo Choo! It's the MysteryTrain!"), channel )
         if (command[0] == "poo"):
            self.sendMessage2Channel( ("Don't be a potty mouth"), channel )
         if (command[0] == "true"):
            self.sendMessage2Channel( ("0 ist false, alles andere true"), channel )
         if (command[0] == "false"):
            self.sendMessage2Channel( ("0 ist false, alles andere true"), channel )