# DADSA - Assignment 1
# Reece Benson

class Round():
    _app = None
    _name = None
    _gender = None
    _matches = [ ]

    def __init__(self, app, gender, name):
        # Set our application
        self._app = app

        # Debug
        if(self.app.debug):
            print("[LOAD] Round: {}".format(name))

        # Set our variables
        self._name = name
        self._gender = gender

    def add_match(self, match):
        self._matches.append(match)

    def matches(self):
        return self._matches

    def match_count(self):
        return len(self.matches())

    def winners(self):
        _winners = [ w for w in self.matches()) if(w.winner()) ]
        return _winners
