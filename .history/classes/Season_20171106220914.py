# DADSA - Assignment 1
# Reece Benson

class Season():
    app = None
    name = None
    players = { }
    rounds = { }

    def __init__(self, _app, name):
        # Set our application as a variable
        self.app = _app

        # Debug
        if(self.app.debug):
            print("[LOAD]: Loaded Season '{0}'".format(name))

        # Set variables
        self.name = name

    def name(self):
        return self.name

    def players(self):
        return self.players

    def rounds(self):
        return self.rounds

    def add_round(self, rnd):
        print(type(rnd))