#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MessageHandler(object):
    @staticmethod
    def norm_channel(channel):
        if channel[0] == "#":
            return channel
        return "#" + channel

    def send(self, data):
        pass

    def send_message(self, data, receiver):
        self.send(("PRIVMSG %s :%s\r\n" % (receiver, data)).encode())

    def send_notice(self, data, receiver):
        self.send(("NOTICE %s :%s\r\n" % (receiver, data)).encode())

    def join_channel(self, channel):
        channel = self.norm_channel(channel)
        self.send("JOIN {0} \r\n".format(channel).encode())
        self.send("PRIVMSG chanserv :op {0} \r\n".format(channel).encode())
        print("NOTICE: Trying to obtain operator status with Chanserv on %s" % channel)
        # This needs to test if the channel is full
        # This needs to modify the list of active channels

    def quit_channel(self, channel):
        channel = self.norm_channel(channel)
        self.send("PART {0} \r\n".format(channel).encode())
        # This needs to modify the list of active channels
