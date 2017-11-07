# DADSA - Assignment 1
# Reece Benson

class Round():
    _app = None
    _name = None
    _gender = None
    _matches = [ ]
    _cap = 3

    def __init__(self, app, gender, name):
        # Set our application
        self._app = app

        # Debug
        if(self._app.debug):
            print("[LOAD] Round: {}".format(name))

        # Set our variables
        self._name = name
        self._gender = gender

    def name(self):
        return self._name

    def gender(self):
        return self._gender

    def cap(self):
        return self._cap

    def set_cap(self, cap):
        self._cap = cap
        return self.cap()

    def add_match(self, match=None):
        self._matches.append(match)

    def matches(self):
        return self._matches or None

    def match_count(self):
        return len(self.matches())

    def winners(self):
        _winners = [ w.winner()[0] for w in self.matches() ]
        return _winners