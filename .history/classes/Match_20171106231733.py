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

    def setPlayers(self, plyrA, plyrB):
        self.playerA = plyrA
        self.playerB = plyrB

    def getWinner(self):
        if(self.playerA.getScore(self.getName()) > self.playerB.getScore(self.getName())):
            self.matchData['winner'] = self.playerA
        else:
            self.matchData['winner'] = self.playerB

        self.winnerSet = True
        return self.matchData['winner']

    def printMatch(self, force = False, ret = False):
        if(not self.winnerSet):
            self.getWinner()

        if(debug or force):
            if(ret):
                return "Match Data: [{2}] {0}:{1} [{3}]".format(self.playerA.getScore(self.matchRound.getName()), self.playerB.getScore(self.matchRound.getName()), self.playerA.getName(), self.playerB.getName())
            else:
                print("Match Data: [{2}] {0}:{1} [{3}]".format(self.playerA.getScore(self.matchRound.getName()), self.playerB.getScore(self.matchRound.getName()), self.playerA.getName(), self.playerB.getName()))
            