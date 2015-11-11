__author__ = 'ole'


class Message:
    irc = None
    propagate = True
    # IRC-protocol attributes
    prefix = ""
    command = []
    content = ""
    # IRC-command dependent attributes
    cmd = []  # bot-command within message
    nick = ""
    channel = None

    def __init__(self, irc, message):
        self.irc = irc
        # get prefix (hostname, etc.)
        prefix_end = 0
        if len(message) > 0 and message[0] == ":":
            prefix_end = message.find(" ")
            self.prefix = message[1:prefix_end]
            prefix_end += 1
        # get content
        content_start = message.find(" :")
        if ~content_start:
            self.content = message[content_start + 2:]
            self.command = message[prefix_end:content_start].split(" ")
        else:
            self.command = message[prefix_end:].split(" ")
        # get channel and/or nick
        if len(self.command) > 1 and len(self.command[1]) > 0 and self.command[1][0] == "#":
            self.channel = self.command[1]
        nick_end = self.prefix.find("!")
        if ~nick_end:
            self.nick = self.prefix[0:nick_end]
        # get command
        if self.content[0:irc.command_prefix_len] == irc.command_prefix:
            self.cmd = self.content[irc.command_prefix_len:].split()

    def get_events(self):
        events = ['on_receive']
        if self.command[0] == "PRIVMSG":
            assert len(self.command) > 1
            events.append('on_message')
            if self.command[1] == self.irc.ircNick:
                events.append('on_private_message')
            elif self.channel:
                events.append('on_channel_message')
            if len(self.cmd):
                events.append('on_command')
        elif self.command[0] == "KICK":
            assert len(self.command) > 2
            if self.command[2] == self.irc.ircNick:
                events.append('on_kick')
        elif self.command[0] == "JOIN":
            events.append('on_join')
        elif self.command[0] == "PING":
            events.append('on_ping')
        elif self.command[0] == "NOTICE":
            events.append('on_notice')
        elif self.command[0] in ["QUIT", "PART"]:
            events.append('on_quit')
        return events

    def __str__(self):
        return "Message[{0}] <{1}>: {2}".format(" ".join(self.command), self.prefix, self.content)
