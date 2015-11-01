Ezrael
======

Ezrael is a simple IRC bot written in Python

[![Codeship Status for Bornageek/Ezrael](https://codeship.io/projects/6dce54f0-624f-0133-e0c3-32b67f1e3a7d/status)](https://codeship.io/projects/112619)

## Installation

To install Ezrael you should first download the sources from GitHub:

    $ git clone https://github.com/Avedo/Ezrael

Then you configure the name and other parameters in the ezrael.ini configuration file. Finally you can start Ezrael using

    $ python3 main.py

You can overwrite the default configuration within a *ezrael.custom.ini* if you don't like to change repository-related files.

## License

The Ezrael IRC bot is licensed under the terms of the Apache License 2.0.

## Todo

- [ ] Simple restart command 
- [ ] Rehash (Reload Plugins to prevent bot from reconnecting)
- [ ] Channel db (Allow different channels with different coinfigurations)
- [ ] Reply to admin commands just via /msg and via /notice 
- [ ] Implement !help and !command commands
- [ ] Extend mensa plugin to accept gps coordinates and radius
- [ ] Implement extra thread for listening
- [ ] Allow setting of context variables in config
- [ ] Reimplement message class
- [ ] Implement automatoic config reading for plugins

## Plugin Ideas

- Calculator (!calc <expression>)
- Sudoku Generator (!sudoku)
- Last seen (!lastseen <username>)
- Messages since last visit (!missed)
- User statistics, like most posts, most online time, etc. (!stats)
- List of upcoming films in Cinemaxx (!kino <city>)
- List of meals in the local mensa (!mensa <city> <mensa> <day>)
- King of the Week (!fastfood)
- FOAAS - Fuck Off As A Service (!foaas <api-paths>)
