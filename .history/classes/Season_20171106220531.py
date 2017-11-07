# DADSA - Assignment 1
# Reece Benson

class Season():
    app = None
    name = None
    players = { }
    rounds = { }

    def __init__(self, _app, name):
        self.app = _app
        if(_app.debug):
            print("FUCK YOU!")

    def add_round(self, rnd):
        print(type(rnd))