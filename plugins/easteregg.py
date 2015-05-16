from core.plugin import Plugin
from core.colors import Color


class EasterEgg(Plugin):
    def onMsg(self, irc, channel, nick, msg):
        # Ensure that the given message starts with a command.
        if msg[0] != '!':
            return

        # Extract the current command.
        command = msg[1:].split()[0].strip().lower()

        if command == "moo":
            irc.sendMessage2Channel("MOO yourself, " + nick, channel)
        elif command == "xkcd":
            irc.sendMessage2Channel("https://c.xkcd.com/random/comic/", channel)
        elif command == "train":
            irc.sendMessage2Channel("Choo Choo! It's the Mystery Train!", channel)
        elif command == "poo":
            irc.sendMessage2Channel("Don't be a potty mouth", channel)
        elif command == "duck":
            irc.sendMessage2Channel("__(\"<", channel)
            irc.sendMessage2Channel("\__/", channel)
            irc.sendMessage2Channel(" ^^", channel)
            irc.sendMessage2Channel("DUCKTALES UhhhHuuuuuuu", channel)
        elif command == "tux":
            irc.sendMessage2Channel("    .--.", channel)
            irc.sendMessage2Channel("   |o_o |", channel)
            irc.sendMessage2Channel("   |:_/ |", channel)
            irc.sendMessage2Channel("  //   \\ \\", channel)
            irc.sendMessage2Channel(" (|     | )", channel)
            irc.sendMessage2Channel("/'\\_   _/`\\", channel)
            irc.sendMessage2Channel("\\___)=(___/", channel)
        elif command == "arch":
            irc.sendMessage2Channel("                  -`", channel)
            irc.sendMessage2Channel("                 .o+`", channel)
            irc.sendMessage2Channel("                `ooo/", channel)
            irc.sendMessage2Channel("               `+oooo:", channel)
            irc.sendMessage2Channel("              `+oooooo:", channel)
            irc.sendMessage2Channel("              -+oooooo+:", channel)
            irc.sendMessage2Channel("            `/:-:++oooo+:", channel)
            irc.sendMessage2Channel("           `/++++/+++++++:", channel)
            irc.sendMessage2Channel("          `/++++++++++++++:", channel)
            irc.sendMessage2Channel("         `/+++ooooooooooooo/`", channel)
            irc.sendMessage2Channel("        ./ooosssso++osssssso+`", channel)
            irc.sendMessage2Channel("       .oossssso-````/ossssss+`", channel)
            irc.sendMessage2Channel("      -osssssso.      :ssssssso.", channel)
            irc.sendMessage2Channel("     :osssssss/        osssso+++.", channel)
            irc.sendMessage2Channel("    /ossssssss/        +ssssooo/-", channel)
            irc.sendMessage2Channel("  `/ossssso+/:-        -:/+osssso+-", channel)
            irc.sendMessage2Channel(" `+sso+:-`                 `.-/+oso:", channel)
            irc.sendMessage2Channel("`++:.                           `-/+/", channel)
            irc.sendMessage2Channel(".`                                 `", channel)
        elif command == "archlinux":
            irc.sendMessage2Channel("       .", channel)
            irc.sendMessage2Channel("      /#\\", channel)
            irc.sendMessage2Channel("     /###\\                     #     | *", channel)
            irc.sendMessage2Channel("    /p^###\\      a##e #%\" a#\"e 6##%  | | |-^-. |   | \\ /", channel)
            irc.sendMessage2Channel("   /##P^q##\\    .oOo# #   #    #  #  | | |   | |   |  X", channel)
            irc.sendMessage2Channel("  /##(   )##\\   %OoO# #   %#e\" #  #  | | |   | ^._.| / \\ TM", channel)
            irc.sendMessage2Channel(" /###P   q#,^\\", channel)
            irc.sendMessage2Channel("/P^         ^q\\ TM", channel)
        elif command == "duckduck":
            irc.sendMessage2Channel(".......ENTE......:", channel)
            irc.sendMessage2Channel(":       ,~~.     :", channel)
            irc.sendMessage2Channel("E      (  6 )-_, E", channel)
            irc.sendMessage2Channel("N (\___ )=='-'   N", channel)
            irc.sendMessage2Channel("T  \ .   ) )     T", channel)
            irc.sendMessage2Channel("E   \ `-' /      E", channel)
            irc.sendMessage2Channel(": ~~'`~'`~'`~`~' :", channel)
            irc.sendMessage2Channel(":......ENTE......:", channel)
        elif command == "gurke":
            irc.sendMessage2Channel("   ".           ,#  ", channel)
            irc.sendMessage2Channel("   \ `-._____,-'=/", channel)
            irc.sendMessage2Channel("____`._ ----- _,'_____PhS", channel)
            irc.sendMessage2Channel("       `-----'", channel)
        elif command == "avedo":

            irc.sendMessage2Channel("   ]j                     TL", channel)
            irc.sendMessage2Channel("   ]j                     wL", channel)
            irc.sendMessage2Channel("   [L NYCLvLvLvLLLvLL]*I4 *v", channel)
            irc.sendMessage2Channel(" *LLvLLLLLLLLLLLLLLLLLLLLLLL?R", channel)
            irc.sendMessage2Channel("lLLLLLLLLLLLLLLLLLLLLLLLLLLLLLl", channel)
            irc.sendMessage2Channel("LLLLLLLLLLLLLLLLLLLLLLLLLLLLL?l", channel)
            irc.sendMessage2Channel("vv       $|?[LLLLL?jQ$      *Uv", channel)
            irc.sendMessage2Channel("vL          *LLLL?          %Lv", channel)
            irc.sendMessage2Channel("v?I         jLLLLL*         jLL", channel)
            irc.sendMessage2Channel("vLLjE     CLLLLLvLL?T     *LLLL", channel)
            irc.sendMessage2Channel("[LvLLLLLLLLLL    wLLLLLLLvLLvL@", channel)
            irc.sendMessage2Channel("  @LvLvvLLLLLLL[LLLLLLLLLvLj", channel)

