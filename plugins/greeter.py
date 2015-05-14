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

  def onMsg(self, irc, channel, nick, msg):
    # Define the greetiungs pattern.
    pattern = re.compile('[hH]([eE3aA4]([yY]|[lL1]{2}[oO0])|[iI])|[mM][oO0][iI][nN]|[oO0][lL1]{1,2}[eE3aA4]')

    if pattern.match(msg) != None:
      greeting = Greeter.greetings[random.randint(0, len(Greeter.greetings)-1)]

      if nick.strip().lower() in irc.fetchAdmins():
        nick = "Master"

      irc.sendMessage2Channel("{0}, {1}".format(greeting, nick), channel)