# DADSA - Assignment 1
# Reece Benson

class Tournament():
    _app = None
    _name = None
    _prize_money = None
    _difficulty = None

    def __init__(self, app, name):
        # Set our Application
        self._app = app

        # Set our variables
        self._name = name
