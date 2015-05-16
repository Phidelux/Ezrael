from core.plugin import Plugin
import random
import re

class Greeter(Plugin):

  greetings = [
    "Ahlan", "Marhaba", "Mirdita", "Tungjatjeta", "Namaskar",
    "Ni hao", "Hello", "Hi", "Saluton", "Tere",
    "Hej", "Salam", "Bula", "Terve", "Hei",
    "Moi", "Moro", "Salut", "Bonjour", "Ja",
    "Aloha", "Schalom", "Namaste", "Ciao", "Buongiorno",
    "Halo", "Konnichi wa", "Tchum-reaup Suw", "Annyeong Haseyo",
    "Ave", "Salve", "Cau", "Sveiki", "Labas",
    "Salama", "Hai", "Tena Koe", "Hallo", "Hoi",
    "Hei", "Hallo", "Morn", "Ola", "Salut",
    "Buna ziua", "Buna", "Hej", "Halla", "Hoi",
    "Sali", "Tschau", "Hallo", "Zdravo", "Ahoj",
    "Halo", "Hola", "Nazdar", "Ahoj", "Merhaba",
    "Priwit", "Szia", "Szervusz"
  ]

  greeted = {}

  def onMsg(self, irc, channel, nick, msg):
    # Define the greetiungs pattern.
    pattern = re.compile('(?xi)^([h]([e3a4]([y]|[l1]{2}[o0])|[i])|[m][o0][i][n]|[o0][l1]{1,2}[a4])$')

    if pattern.match(msg) != None:

      if channel not in self.greeted:
        self.greeted[channel] = []

      if nick not in self.greeted[channel]:

        greeting = Greeter.greetings[random.randint(0, len(Greeter.greetings)-1)]

        if nick.strip().lower() in irc.fetchAdmins():
          nick = "Master"
        else:
          self.greeted[channel].append(nick)

        irc.sendMessage2Channel("{0}, {1}".format(greeting, nick), channel)