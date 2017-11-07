# DADSA - Assignment 1
# Reece Benson

class Match():
    _round = None
    _winner = None
    _player_one = None
    _player_two = None
    _player_one_score = None
    _player_two_score = None
    
    def __init__(self, rnd, p_one, p_two, p_one_score, p_two_score):
        self._round = rnd
        self._player_one = p_one
        self._player_two = p_two
        self._player_one_score = p_one_score
        self._player_two_score = p_two_score
        
    def round(self):
        return self._round

    def player_one(self):
        return { "player": self._player_one, "score": self._player_one_score }

    def player_two(self):
        return { "player": self._player_two, "score": self._player_two_score }

    def versuses(self):
        return "{0} vs. {1}".format(self.player_one()['player'].name(), self.player_two()['player'].name())

    def winner(self):
        if(self._player_one_score > self._player_two_score):
            self._winner = self.player_one().player
            return self.player_one()
        else:
            self._winner = self.player_two().player
            return self.player_two()