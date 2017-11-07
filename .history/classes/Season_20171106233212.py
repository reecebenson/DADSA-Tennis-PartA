# DADSA - Assignment 1
# Reece Benson

from classes import Player as Player

class Season():
    _app = None
    _j_data = None
    _name = None
    _players = { }
    _rounds = { }
    _rounds_raw = { }
    _settings = { }

    def __init__(self, _app, name, j_data):
        # Set our application as a variable
        self._app = _app
        
        # Set our Season JSON Data in a variable
        self._j_data = j_data

        # Debug
        if(self._app.debug):
            print("[LOAD]: Loaded Season '{0}'".format(name))

        # Set variables
        self._name = name
        self._settings = j_data['settings']

    def name(self):
        return self._name

    def settings(self):
        return self._settings

    def players(self):
        return self._players

    def add_player(self, name, gender):
        if(not gender in self.players()):
            self._players[gender] = [ ]

        # Append our Players to their specific gender category
        self._players[gender].append(Player.Player(name, gender, len(self.players()[gender])))

    def rounds(self):
        return self._rounds

    def set_rounds(self):
        for rnd in self._rounds_raw:
            for gdr in self._rounds_raw[rnd]:
                # If the Gender category doesn't exist within the rounds, create it
                if(not gdr in self._rounds):
                    self._rounds[gdr] = [ ]

                # Populate our dictionary with our match data
                for match in self._rounds_raw[rnd][gdr]:
                    print(match)
                    if("roundCap" in match):
                        continue

                    self._rounds[gdr].append(match)
                    break
        print(self._rounds)
                
    def set_rounds_raw(self, rounds):
        self._rounds_raw = rounds
        self.set_rounds()
