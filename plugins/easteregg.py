from core.plugin import Plugin

# DEPRECATED. TODO: save those Easter-Eggs using record plugin

class EasterEgg(Plugin):
    def onMsg(self, irc, channel, nick, msg):
        # Ensure that the given message starts with a command.
        if msg[0] != '!':
            return

        # Extract the current command.
        command = msg[1:].split()[0].strip().lower()

        if command == "moo":
            self.send_message("MOO yourself, " + nick, channel)
        elif command == "xkcd":
            self.send_message("https://c.xkcd.com/random/comic/", channel)
        elif command == "train":
            self.send_message("Choo Choo! It's the Mystery Train!", channel)
        elif command == "poo":
            self.send_message("Don't be a potty mouth", channel)
        elif command == "duck":
            self.send_message("__(\"<", channel)
            self.send_message("\__/", channel)
            self.send_message(" ^^", channel)
            self.send_message("DUCKTALES UhhhHuuuuuuu", channel)
        elif command == "tux":
            self.send_message("    .--.", channel)
            self.send_message("   |o_o |", channel)
            self.send_message("   |:_/ |", channel)
            self.send_message("  //   \\ \\", channel)
            self.send_message(" (|     | )", channel)
            self.send_message("/'\\_   _/`\\", channel)
            self.send_message("\\___)=(___/", channel)
        elif command == "arch":
            self.send_message("                  -`", channel)
            self.send_message("                 .o+`", channel)
            self.send_message("                `ooo/", channel)
            self.send_message("               `+oooo:", channel)
            self.send_message("              `+oooooo:", channel)
            self.send_message("              -+oooooo+:", channel)
            self.send_message("            `/:-:++oooo+:", channel)
            self.send_message("           `/++++/+++++++:", channel)
            self.send_message("          `/++++++++++++++:", channel)
            self.send_message("         `/+++ooooooooooooo/`", channel)
            self.send_message("        ./ooosssso++osssssso+`", channel)
            self.send_message("       .oossssso-````/ossssss+`", channel)
            self.send_message("      -osssssso.      :ssssssso.", channel)
            self.send_message("     :osssssss/        osssso+++.", channel)
            self.send_message("    /ossssssss/        +ssssooo/-", channel)
            self.send_message("  `/ossssso+/:-        -:/+osssso+-", channel)
            self.send_message(" `+sso+:-`                 `.-/+oso:", channel)
            self.send_message("`++:.                           `-/+/", channel)
            self.send_message(".`                                 `", channel)
        elif command == "archlinux":
            self.send_message("       .", channel)
            self.send_message("      /#\\", channel)
            self.send_message("     /###\\                     #     | *", channel)
            self.send_message("    /p^###\\      a##e #%\" a#\"e 6##%  | | |-^-. |   | \\ /", channel)
            self.send_message("   /##P^q##\\    .oOo# #   #    #  #  | | |   | |   |  X", channel)
            self.send_message("  /##(   )##\\   %OoO# #   %#e\" #  #  | | |   | ^._.| / \\ TM", channel)
            self.send_message(" /###P   q#,^\\", channel)
            self.send_message("/P^         ^q\\ TM", channel)
        elif command == "duckduck":
            self.send_message(".......ENTE......:", channel)
            self.send_message(":       ,~~.     :", channel)
            self.send_message("E      (  6 )-_, E", channel)
            self.send_message("N (\___ )=='-'   N", channel)
            self.send_message("T  \ .   ) )     T", channel)
            self.send_message("E   \ `-' /      E", channel)
            self.send_message(": ~~'`~'`~'`~`~' :", channel)
            self.send_message(":......ENTE......:", channel)
        elif command == "gurke":
            self.send_message("   #.           ,# ", channel)
            self.send_message("   \ `-._____,-'=/", channel)
            self.send_message("____`._ ----- _,'_____PhS", channel)
            self.send_message("       `-----'", channel)
        elif command == "avedo":
            self.send_message("   ]j                     TL", channel)
            self.send_message("   ]j                     wL", channel)
            self.send_message("   [L NYCLvLvLvLLLvLL]*I4 *v", channel)
            self.send_message(" *LLvLLLLLLLLLLLLLLLLLLLLLLL?R", channel)
            self.send_message("lLLLLLLLLLLLLLLLLLLLLLLLLLLLLLl", channel)
            self.send_message("LLLLLLLLLLLLLLLLLLLLLLLLLLLLL?l", channel)
            self.send_message("vv       $|?[LLLLL?jQ$      *Uv", channel)
            self.send_message("vL          *LLLL?          %Lv", channel)
            self.send_message("v?I         jLLLLL*         jLL", channel)
            self.send_message("vLLjE     CLLLLLvLL?T     *LLLL", channel)
            self.send_message("[LvLLLLLLLLLL    wLLLLLLLvLLvL@", channel)
            self.send_message("  @LvLvvLLLLLLL[LLLLLLLLLvLj", channel)
