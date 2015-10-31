from core.msghandler import MessageHandler
from queue import *
import _thread
import time

class Plugin(MessageHandler):
    def __init__(self, context=None):
        self.context = context
        self.queue_in = Queue()
        self.queue_out = Queue()
        _thread.start_new_thread(self.run,())
        self.resttime = 0
        self.lastcmd = 0

    def run(self):
        while True:
            event, args, kwargs = self.queue_in.get()

            try:
                getattr(self, event)(*args, **kwargs) 
            except IndexError:
                print("IndexError")
                pass
            except ValueError:
                print("ValueError")
                pass

    def queue(self, event, *args, **kwargs):
        self.queue_in.put((event, args, kwargs))

    def send(self, data):
        self.queue_out.put(data)

    def init(self):
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
