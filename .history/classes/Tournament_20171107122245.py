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

    def name(self):
        return self._name

    def prize_money(self):
        return self._prize_money

    def set_prize_money(self, prize_money):
        self._prize_money = prize_money

    def difficulty(self):
        return self._difficulty

    def set_difficulty(self, difficulty):
        self._difficulty = difficulty
