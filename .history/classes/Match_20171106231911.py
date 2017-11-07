# DADSA - Assignment 1
# Reece Benson

class Match():
    _round = None
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
        return [ self._player_one, self._player_one_score ]

    def player_two(self):
        return [ self._player_two, self._player_two_score ]

    def winner(self):
        if(self._player_one_score > self._player_two_score):
            return self.player_one()
        else:
            return self.player_two()

    def getWinner(self):
        if(self.playerA.getScore(self.getName()) > self.playerB.getScore(self.getName())):
            self.matchData['winner'] = self.playerA
        else:
            self.matchData['winner'] = self.playerB

        self.winnerSet = True
        return self.matchData['winner']