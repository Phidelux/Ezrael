#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import getopt
import threading
import time

from core.ezrael import Ezrael

def usage():
    print('Usage: python ezrael.py [-h]\n\n'
          '-h\tShows this help'
          '-v\tVersion of ezrael'
          '-d\tTurn on debugging')

def main(argv):
    debugging = False

    try:
        opts, args = getopt.getopt(argv, "hvd", ["help", "version", "debug"])
    except getopt.GetoptError as err:
        # Print usage information and exit.
        print(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif o in ("-v", "--version"):
            print("Version 0.1")
            sys.exit(1)
        elif o in ("-d", "--debug"):
            debugging = True
        else:
            assert False, "unhandled option"

    try:
        # Initialize the irc bot, ...
        ezrael = Ezrael(debugging)

        # ... bind the connect method of ezrael to a thread, ...
        ezrael_thread = threading.Thread(None, ezrael.connect)

        # ... make this thread a daemon thread ...
        ezrael_thread.setDaemon(True)

        # ... and start the IRC bot.
        ezrael_thread.start()

        # Enter a loop if you should try to reconnect.
        while ezrael.shouldReconnect:
            time.sleep(5)
    except:
        pass
    finally:
        print('Goodbye!')

if __name__ == "__main__":
    main(sys.argv[1:])
