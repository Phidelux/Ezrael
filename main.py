from core.ezrael import Ezrael
import sys, getopt
import threading
import time

def usage():
    print( 'Usage: python ezrael.py [-h]\n\n' \
          '-h\tShows this help' );

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError as err:
        # Print usage information and exit.
        print(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(1)
        else:
            assert False, "unhandled option"

    # Initialize the irc bot, ...
    ezrael = Ezrael()

    # ... bind the connect method of ezrael to a thread ...
    runEzrael = threading.Thread(None, ezrael.connect)

    # ... and start the IRC bot.
    runEzrael.start()

    # Enter a loop if you should try to reconnect.
    while (ezrael.shouldReconnect):
        time.sleep(5)

if __name__ == "__main__":
    main(sys.argv[1:])
