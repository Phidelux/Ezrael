from core.plugin import Plugin
import random


class VoteInstance():
    def __init__(self, print_lambda):
        self.voted = {}  # {nick: {option: vote}}
        self.votes_valid = {}
        self.votes_invalid = {}
        self.modes = {
            'verbose': 0,
            'change': True,
            'collect': False,
            'multiple': False,
            'random': True
        }
        self.mode = {
            'c': 'change',
            'o': 'collect',
            'm': 'multiple',
            'r': 'random'
        }
        self.count_valid = 0
        self.count_invalid = 0
        self._p = print_lambda
        self.title = ""

    def init(self, args):
        self.title = args[0].strip()
        self._p("Voting started. Vote with '!vote OPTION'.")
        self._p(" -- {0}".format(self.title))
        if len(args) > 1:
            arg = args[1].strip()
            if arg[0] == ':':
                self.set_modes(arg[1:])
            else:
                self.add_option(arg)
        for option in args[2:]:
            self.add_option(option.strip())
        if not len(self.votes_valid):
            self.modes['collect'] = True

    def set_modes(self, modes):
        for mode in modes:
            if mode == 'v':
                self.modes['verbose'] += 1
            elif mode == 'V':
                self.modes['verbose'] -= 1
            elif mode in self.mode:
                self.modes[self.mode[mode]] = True
            else:
                # if mode given in uppercase set to false
                mode = mode.lower()
                if mode in self.mode:
                    self.modes[self.mode[mode]] = False

    def add_option(self, option):
        self._p(" -- -- {0}".format(option))
        self.votes_valid[option] = 0

    def may_vote(self, nick, option):
        if option[0] == '-':
            option = option[1:].strip()
            return self.modes['change'] and nick in self.voted and self.voted[nick][option] > 0
        return nick not in self.voted or (self.modes['multiple'] and option not in self.voted[nick])

    def vote(self, nick, option):
        # read arguments
        value = 1
        if option[0] == '-':
            option = option[1:].strip()
            value = -1
        # update vote-status of nick
        if nick not in self.voted:
            self.voted[nick] = {}
        if option not in self.voted[nick]:
            self.voted[nick][option] = value
        else:
            self.voted[nick][option] += value
        # tidy up (e.g. if vote got reverted)
        if self.voted[nick][option] == 0:
            del self.voted[nick][option]
            if not len(self.voted[nick]):
                del self.voted[nick]
        # add value to respective option
        if option in self.votes_valid:
            self.votes_valid[option] += value
            self.count_valid += value
        else:
            if option in self.votes_invalid:
                self.votes_invalid[option] += value
            else:
                self.votes_invalid[option] = value
            self.count_invalid += value

    def print_result(self, votes, winners, count):
        if len(winners):
            if count > 0:
                quote = votes[winners[0]] / count * 100
            else:
                quote = 0
            if self.modes['random'] or len(winners) == 1:
                winner = random.choice(winners)
                if self.modes['verbose'] >= 1:
                    self._p(" -- Result: {0} ({1}% out of {2} votes)".format(winner, ('%.2f' % quote), count))
                else:
                    self._p(" -- Result: {0}".format(winner))
            else:
                if self.modes['verbose'] >= 1:
                    self._p(" -- Results: {0} (each {1}% out of {2} votes)".format(winners, ('%.2f' % quote), count))
                else:
                    self._p(" -- Results: {0}".format(winners))
        else:
            self._p(" -- No result")

    def print_ordered(self, votes):
        items = [item for item in votes.items()]
        items.sort(key=lambda x: x[1])
        items.reverse()
        for item in items:
            self._p(" -- -- {0}: {1}".format(item[1], item[0]))

    def print(self):
        votes_valid = self.votes_valid
        votes_invalid = self.votes_invalid
        votes_both = {}
        for option in votes_valid:
            votes_both[option] = votes_valid[option]
        for option in votes_invalid:
            votes_both[option] = votes_invalid[option]

        if len(votes_valid):
            max_val_valid = votes_valid[max(votes_valid, key=lambda x: votes_valid[x])]
        else:
            max_val_valid = 0
        if len(votes_invalid):
            max_val_invalid = votes_invalid[max(votes_invalid, key=lambda x: votes_invalid[x])]
        else:
            max_val_invalid = 0
        max_val_both = max(max_val_invalid, max_val_valid)

        count_valid = self.count_valid
        count_invalid = self.count_invalid
        count_both = count_invalid + count_valid

        self._p("Voting ended: {0}".format(self.title))

        if self.modes['collect']:
            winners_both = [option for option in votes_both if votes_both[option] == max_val_both]
            self.print_result(votes_both, winners_both, count_both)
        else:
            winners_valid = [option for option in votes_valid if votes_valid[option] == max_val_valid]
            self.print_result(votes_valid, winners_valid, count_valid)

        if self.modes['verbose'] == 2:
            if self.modes['collect']:
                self.print_ordered(votes_both)
            else:
                self.print_ordered(votes_valid)
        elif self.modes['verbose'] >= 3:
            if len(votes_valid):
                self._p(" -- {0} valid votes:".format(count_valid))
                self.print_ordered(votes_valid)
            if len(votes_invalid):
                self._p(" -- {0} invalid votes:".format(count_invalid))
                self.print_ordered(votes_invalid)
            if len(votes_valid) and len(votes_invalid):
                self._p(" -- {0} votes at all:".format(count_both))
                self.print_ordered(votes_both)


class Voting(Plugin):
    def __init__(self, config):
        super().__init__(config)
        self.help_commands = {
            'vote': 'OPTION - Vote for OPTION',
            'votestart': 'TITLE[,:MODES][,OPTION[,OPTION[,...]]] - Start a new voting.'
                         ' Modes: verbose (v), change (c), collect (o), multiple (m), random (r)',
            'voteend': '[MODES] - End the current voting and print results.'
                       ' Modes: verbose (v), collect (o), random (r)'
        }
        self.ezrael = None
        self.votings = {}

    def init(self, ezrael):
        self.ezrael = ezrael

    def msg(self, nick, message):
        self.ezrael.send_message(message, nick)

    def on_command(self, irc, message):
        if message.cmd[0] not in self.help_commands:
            return

        if message.cmd[0] == 'vote':
            option = " ".join(message.cmd[1:])
            if message.channel not in self.votings:
                self.send_message("No active voting (within message.channel {0}).".format(message.channel), message.nick)
            elif self.votings[message.channel].may_vote(message.nick, option):
                self.votings[message.channel].vote(message.nick, option)
            else:
                self.msg(message.nick, "You're not supposed to vote for {0}.".format(option))
        else:
            if message.nick.lower() in self.ezrael.admins:
                if message.cmd[0] == 'votestart':
                    if message.channel in self.votings:
                        self.votings[message.channel].print()
                    self.votings[message.channel] = VoteInstance(lambda x: self.send_message(x, message.channel))
                    self.votings[message.channel].init(" ".join(message.cmd[1:]).strip().split(","))
                    return
                elif message.cmd[0] == 'voteend':
                    if message.channel not in self.votings:
                        self.msg(message.nick, "No active voting (within message.channel {0}).".format(message.channel))
                    else:
                        self.votings[message.channel].set_modes("".join(message.cmd[1:]).strip())
                        self.votings[message.channel].print()
                        del self.votings[message.channel]
            else:
                self.msg(message.nick, "Operation not permitted.")
