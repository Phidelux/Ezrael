#!/usr/bin/env python
# This code was written for Python 3.4
# version 0.101

# Changelog:
# version 0.1
#
# version 0.1
# Restructured the complete base code

import socket, sys, threading, time, getopt, dns.resolver

# Defining a class to run the server. One per connection. This class will do most of our work.
class Ezrael:
    # The default constructor - declaring global variables
    # channel should be rewritten to be a list, which then loops to connect, per channel.
    # This needs to support an alternate nick.
    def __init__(self, host, port, channel, nick, password = ""):
        self.ircHost = host
        self.ircPort = port
        self.ircNick = nick
        self.ircPassword = password
        self.ircChannel = channel
        self.ircSock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.isConnected = False
        self.shouldReconnect = False
        self.command = ""

    # This is the bit that controls connection to a server & channel.
    # It should be rewritten to allow multiple channels in a single server.
    # This needs to have an "auto identify" as part of its script, or support a custom connect message.
    def connect(self):
        self.shouldReconnect = True
        try:
            self.ircSock.connect((self.ircHost, self.ircPort))
        except:
            print ("Error: Could not connect to IRC; Host: " + str(self.ircHost) + "Port: " + str(self.ircPort))
            exit(1) # TODO: We should make it reconnect if it gets an error here
        print ("Connected to: " + str(self.ircHost) + ":" + str(self.ircPort))

        buffer = ("NICK %s \r\n" % self.ircNick)
        self.ircSock.send (buffer.encode())
        print ("Setting bot nick to " + str(self.ircNick) )

        buffer = ("USER %s 8 * :X\r\n" % self.ircNick)
        self.ircSock.send (buffer.encode())
        print ("Setting User")
        # Insert Alternate nick code here.

        buffer = ("PRIVMSG nickserv :identify %s %s\r\n" % (self.ircNick, self.ircPassword))
        self.ircSock.send (buffer.encode())
        print ("Nickserv Identify")

        buffer = ( "JOIN %s \r\n"  % self.ircChannel)
        self.ircSock.send (buffer.encode())
        print ("Joining channel " + str(self.ircChannel) )

        buffer = ("PRIVMSG chanserv :op %s \r\n" % self.ircChannel)
        self.ircSock.send (buffer.encode())
        print ("try to op me")

        self.isConnected = True
        self.listen()

    def listen(self):
        while self.isConnected:
            recv = self.ircSock.recv( 500 )

            print (recv)
            if str(recv).find ( "PING" ) != -1:
                self.ircSock.send ( "PONG ".encode() + recv.split() [ 1 ] + "\r\n".encode() )

            # TODO: Welcome message does not work yet.
            if str(recv).find ( "JOIN " + self.ircChannel ) != -1:
                ircUserNick = str(recv).split ( '!' ) [ 0 ] . split ( ":")[1]
                str_buff = ("NOTICE " + ircUserNick + " Welcome in " + self.ircChannel + " Channel. \r\n")
                self.ircSock.send (str_buff.encode())

            if str(recv).find ( "NOTICE" ) != -1:
                ircUserNick = str(recv).split ( '!' ) [ 0 ] . split ( ":")[1]
                ircUserMessage = self.data2message(str(recv))
                print ( "Notice! " + ircUserNick + "->" + ircUserMessage + "\r\n" )

            if str(recv).find ( "PRIVMSG" ) != -1:
                ircUserMessageserNick = str(recv).split ( '!' ) [ 0 ] . split ( ":")[1]
                ircUserHost = str(recv).split ( '@' ) [ 1 ] . split ( ' ' ) [ 0 ]
                ircUserMessage = self.data2message(str(recv))
                print ( ircUserNick + ": " + ircUserMessage)

                # "!" Indicated a command
                if ( str(ircUserMessage[0]) == "!" ):
                    self.command = str(ircUserMessage[1:])
                    # (str(recv)).split()[2] ) is simply the channel the command was heard on.
                    self.processCommand(ircUserNick, ( (str(recv)).split()[2] ) )
                else:
                    self.processMessage(ircUserMessage, ircUserNick, ( (str(recv)).split()[2] ) )
        if self.shouldReconnect:
            self.connect()

    def processMessage(self, data, nickname, channel):
        if (nickname == "Ganktimebaby" and data == "hallo"):
            self.sendMessage2Channel( ("Hallo Gott"), channel )

        elif (data == "hallo"):
            self.sendMessage2Channel( ("Hallo, " + nickname), channel )
        elif (data == "HaLl0" or data == "hall0" or data == "ha110"):
            self.sendMessage2Channel( ("\x01ACTION slaps " + nickname + "around a bit with a large dick\x01"), channel )
        elif (data == "fu" or data == "FU"):
            self.sendMessage2Channel( ("fu dich selber du bengel"), channel )
        elif (data == "slaps Ezrael"):
            self.sendMessage2Channel( ("slap dich selber du schuettelwurm!"), channel )

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
            # This needs to test if the channel is full
            # This needs to modify the list of active channels

    # This function takes a channel, which must start with a #.
    def quitChannel(self,channel):
        if (channel[0] == "#"):
            str_buff = ( "PART %s \r\n" ) % (channel)
            self.ircSock.send (str_buff.encode())
            # This needs to modify the list of active channels
        ### Wiki

    def wiki(self, query):
        query = '_'.join(query).strip().replace(" \t\r\n", "_")
        host = query + '.wp.dg.cx'
        result = ""

        try:
            answers = dns.resolver.query(host, 'TXT')

            for txtRecord in answers.response.answer:
                result = txtRecord.to_text().split('"')[1]
        except dns.resolver.NXDOMAIN as e:
            print (e)
            print ("No such domain %s" % host)
        except dns.resolver.Timeout:
            print ("Timed out while resolving %s" % host)
        except dns.exception.DNSException:
            print ("Unhandled exception")
        return result
    ### wiki


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
        if (user == rootUser):
            if ( len(command) == 1):

                #This command shuts the bot down.
                if (command[0] == "quit"):
                    str_buff = ( "QUIT %s \r\n" ) % (channel)
                    self.ircSock.send (str_buff.encode())
                    self.ircSock.close()
                    self.isConnected = False
                    self.shouldReconnect = False

                elif (command[0] == "op"):
                    str_buff = ("MODE #seekampf +o Ganktimebaby \r\n")
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


            if (command[0] == "moo"):
                self.sendMessage2Channel( ("MOO yourself, " + user), channel )
            if (command[0] == "train"):
                self.sendMessage2Channel( ("Choo Choo! It's the MysteryTrain!"), channel )
            if (command[0] == "poo"):
                self.sendMessage2Channel( ("Don't be a potty mouth"), channel )
            if (command[0] == "readnext"):
                self.sendMessage2Channel( ("Visit whatshouldIreadnext.com"), channel )
        else:
            if (command[0] == "bop"):
                self.sendMessage2Channel( ("\x01ACTION bopz " + str(command[1]) + "\x01"), channel )
            if (command[0] == "wiki"):
                print(self.wiki(command[1:]))
                self.sendMessage2Channel( "[Wikipedia] " + self.wiki(command[1:]), channel )
