from core.msghandler import MessageHandler
from queue import *
import _thread
import time

class Plugin(MessageHandler):
    def __init__(self, config=None):
        self.config = config
        self.queue_in = Queue()
        self.queue_out = Queue()
        _thread.start_new_thread(self.run,())
        self.resttime = 0
        self.lastcmd = 0

    def run(self):
        while True:
            event, message = self.queue_in.get()

            try:
                getattr(self, event)(message) 
            except IndexError:
                print("IndexError")
                pass
            except ValueError:
                print("ValueError")
                pass

    def queue(self, event, message):
        self.queue_in.put((event, message))

    def send(self, data):
        self.queue_out.put(data)

    def init(self, message):
        pass

    def on_receive(self, message):
        pass

    def on_private_message(self, message):
        pass

    def on_channel_message(self, message):
        pass

    def on_message(self, message):
        pass

    def on_command(self, message):
        pass

    def on_kick(self, message):
        pass

    def on_join(self, message):
        pass

    def on_ping(self, message):
        pass

    def on_notice(self, message):
        pass
