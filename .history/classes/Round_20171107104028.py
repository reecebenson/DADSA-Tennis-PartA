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
