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
            irc.send_message("MOO yourself, " + nick, channel)
        elif command == "xkcd":
            irc.send_message("https://c.xkcd.com/random/comic/", channel)
        elif command == "train":
            irc.send_message("Choo Choo! It's the Mystery Train!", channel)
        elif command == "poo":
            irc.send_message("Don't be a potty mouth", channel)
        elif command == "duck":
            irc.send_message("__(\"<", channel)
            irc.send_message("\__/", channel)
            irc.send_message(" ^^", channel)
            irc.send_message("DUCKTALES UhhhHuuuuuuu", channel)
        elif command == "tux":
            irc.send_message("    .--.", channel)
            irc.send_message("   |o_o |", channel)
            irc.send_message("   |:_/ |", channel)
            irc.send_message("  //   \\ \\", channel)
            irc.send_message(" (|     | )", channel)
            irc.send_message("/'\\_   _/`\\", channel)
            irc.send_message("\\___)=(___/", channel)
        elif command == "arch":
            irc.send_message("                  -`", channel)
            irc.send_message("                 .o+`", channel)
            irc.send_message("                `ooo/", channel)
            irc.send_message("               `+oooo:", channel)
            irc.send_message("              `+oooooo:", channel)
            irc.send_message("              -+oooooo+:", channel)
            irc.send_message("            `/:-:++oooo+:", channel)
            irc.send_message("           `/++++/+++++++:", channel)
            irc.send_message("          `/++++++++++++++:", channel)
            irc.send_message("         `/+++ooooooooooooo/`", channel)
            irc.send_message("        ./ooosssso++osssssso+`", channel)
            irc.send_message("       .oossssso-````/ossssss+`", channel)
            irc.send_message("      -osssssso.      :ssssssso.", channel)
            irc.send_message("     :osssssss/        osssso+++.", channel)
            irc.send_message("    /ossssssss/        +ssssooo/-", channel)
            irc.send_message("  `/ossssso+/:-        -:/+osssso+-", channel)
            irc.send_message(" `+sso+:-`                 `.-/+oso:", channel)
            irc.send_message("`++:.                           `-/+/", channel)
            irc.send_message(".`                                 `", channel)
        elif command == "archlinux":
            irc.send_message("       .", channel)
            irc.send_message("      /#\\", channel)
            irc.send_message("     /###\\                     #     | *", channel)
            irc.send_message("    /p^###\\      a##e #%\" a#\"e 6##%  | | |-^-. |   | \\ /", channel)
            irc.send_message("   /##P^q##\\    .oOo# #   #    #  #  | | |   | |   |  X", channel)
            irc.send_message("  /##(   )##\\   %OoO# #   %#e\" #  #  | | |   | ^._.| / \\ TM", channel)
            irc.send_message(" /###P   q#,^\\", channel)
            irc.send_message("/P^         ^q\\ TM", channel)
        elif command == "duckduck":
            irc.send_message(".......ENTE......:", channel)
            irc.send_message(":       ,~~.     :", channel)
            irc.send_message("E      (  6 )-_, E", channel)
            irc.send_message("N (\___ )=='-'   N", channel)
            irc.send_message("T  \ .   ) )     T", channel)
            irc.send_message("E   \ `-' /      E", channel)
            irc.send_message(": ~~'`~'`~'`~`~' :", channel)
            irc.send_message(":......ENTE......:", channel)
        elif command == "gurke":
            irc.send_message("   #.           ,# ", channel)
            irc.send_message("   \ `-._____,-'=/", channel)
            irc.send_message("____`._ ----- _,'_____PhS", channel)
            irc.send_message("       `-----'", channel)
        elif command == "avedo":
            irc.send_message("   ]j                     TL", channel)
            irc.send_message("   ]j                     wL", channel)
            irc.send_message("   [L NYCLvLvLvLLLvLL]*I4 *v", channel)
            irc.send_message(" *LLvLLLLLLLLLLLLLLLLLLLLLLL?R", channel)
            irc.send_message("lLLLLLLLLLLLLLLLLLLLLLLLLLLLLLl", channel)
            irc.send_message("LLLLLLLLLLLLLLLLLLLLLLLLLLLLL?l", channel)
            irc.send_message("vv       $|?[LLLLL?jQ$      *Uv", channel)
            irc.send_message("vL          *LLLL?          %Lv", channel)
            irc.send_message("v?I         jLLLLL*         jLL", channel)
            irc.send_message("vLLjE     CLLLLLvLL?T     *LLLL", channel)
            irc.send_message("[LvLLLLLLLLLL    wLLLLLLLvLLvL@", channel)
            irc.send_message("  @LvLvvLLLLLLL[LLLLLLLLLvLj", channel)
