# DADSA - Assignment 1
# Reece Benson

from classes import Player as Player

class Season():
    _app = None
    _name = None
    _players = { }
    _rounds = { }

    def __init__(self, _app, name):
        # Set our application as a variable
        self._app = _app

        # Debug
        if(self._app.debug):
            print("[LOAD]: Loaded Season '{0}'".format(name))

        # Set variables
        self._name = name

    def name(self):
        return self._name

    def players(self):
        return self._players

    def add_player(self, name, gender):
        if(not gender in self.players()):
            self._players[gender] = [ ]

        self._players[gender].append(name)

    def rounds(self):
        return self._rounds

    def add_round(self, rnd):
        print(type(rnd))