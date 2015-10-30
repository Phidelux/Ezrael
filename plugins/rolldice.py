from core.plugin import Plugin
import random
import re


class RollDice(Plugin):
    def on_command(self, message):
        if message.cmd[0] not in ['dice', 'rolldice', 'coin', 'flipcoin']:
            return

        # Define default values.
        eyes = 6
        times = 1

        if message.cmd[0] in ['coin', 'flipcoin']:
            eyes = 2

            # Define the number pattern ...
            pattern = re.compile(r"(?<![-.])\b[0-9]+\b(?!\.[0-9])")

            # ... and search for numbers in the command.
            matches = pattern.findall(message.content)

            if len(matches) > 0:
                times = max([2, int(matches[0])])
        else:
            # Define the number pattern ...
            pattern = re.compile(r"(?<![-.])\b[0-9]+\b(?!\.[0-9])")

            # ... and search for numbers in the command.
            matches = pattern.findall(message.content)

            if len(matches) > 1:
                eyes = max([2, min([1000000, int(matches[0])])])
                times = max([1, min([10, int(matches[1])])])
            elif len(matches) > 0:
                eyes = max([2, min([1000000, int(matches[0])])])

        if eyes == 42:
            self.send_message("This is the Answer to The Ultimate Question of Life, the Universe, and Everything!",
                             message.channel)
        elif eyes != 20 or times > 1:
            results = []
            for i in range(0, times):
                results.append(str(random.randint(1, eyes)))

            self.send_message(", ".join(results), message.channel)
        else:
            result = random.randint(1, eyes)

            if result == 1:
                self.send_message("1 -> CRITICAL!", message.channel)
            elif result == 20:
                self.send_message("20 -> FLOP! YOU GET BEATEN UP!", message.channel)
            else:
                self.send_message("{0}".format(result), message.channel)
