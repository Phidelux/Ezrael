from core.plugin import Plugin
from core.colors import Color

class Rainbow(Plugin):
    def on_command(self, message):
        # Extract the current command and message ...
        command = message.cmd[0]
        msg = message.content[self.context['command_prefix_len'] + len(command):].strip()

        # ... and print the colorized version.
        if command == "black":
            self.send_message("{0}{1}".format(Color.black, msg), message.channel)
        elif command == "blue":
            self.send_message("{0}{1}".format(Color.navy_blue, msg), message.channel)
        elif command == "green":
            self.send_message("{0}{1}".format(Color.green, msg), message.channel)
        elif command == "red":
            self.send_message("{0}{1}".format(Color.red, msg), message.channel)
        elif command == "brown":
            self.send_message("{0}{1}".format(Color.brown, msg), message.channel)
        elif command == "purple":
            self.send_message("{0}{1}".format(Color.purple, msg), message.channel)
        elif command == "olive":
            self.send_message("{0}{1}".format(Color.olive, msg), message.channel)
        elif command == "yellow":
            self.send_message("{0}{1}".format(Color.yellow, msg), message.channel)
        elif command == "lime_green":
            self.send_message("{0}{1}".format(Color.lime_green, msg), message.channel)
        elif command == "teal":
            self.send_message("{0}{1}".format(Color.teal, msg), message.channel)
        elif command == "aqua_light":
            self.send_message("{0}{1}".format(Color.aqua_light, msg), message.channel)
        elif command == "royal_blue":
            self.send_message("{0}{1}".format(Color.royal_blue, msg), message.channel)
        elif command == "hot_pink":
            self.send_message("{0}{1}".format(Color.hot_pink, msg), message.channel)
        elif command == "dark_gray":
            self.send_message("{0}{1}".format(Color.dark_gray, msg), message.channel)
        elif command == "light_gray":
            self.send_message("{0}{1}".format(Color.light_gray, msg), message.channel)
        elif command == "white":
            self.send_message("{0}{1}".format(Color.white, msg), message.channel)
        elif command == "bold":
            self.send_message("{0}{1}".format(Color.bold, msg), message.channel)
        elif command == "italic":
            self.send_message("{0}{1}".format(Color.italic, msg), message.channel)
        elif command == "underline":
            self.send_message("{0}{1}".format(Color.underline, msg), message.channel)
        elif command == "underline2":
            self.send_message("{0}{1}".format(Color.underline2, msg), message.channel)
        elif command == "reverse":
            self.send_message("{0}{1}".format(Color.reverse, msg), message.channel)
        elif command == "strike":
            self.send_message("{0}{1}".format(Color.strike_through, msg), message.channel)
        elif command == "rainbow" and msg != '':
            rainbow_msg = ''
            for i in range(0, len(msg)):
                rainbow_msg += "{0}{1}".format(Color.random(), msg[i])
            rainbow_msg += "{0}".format(Color.clear)
            self.send_message(rainbow_msg, message.channel)
        elif command == "rainbow":
            self.send_message(
                "I love {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}!".format(
                    Color.black, 'R', Color.navy_blue, 'A', Color.green, 'I',
                    Color.red, 'N', Color.purple, 'B', Color.yellow, 'O',
                    Color.teal, 'W', Color.hot_pink, 'S', Color.clear
                ), message.channel)
