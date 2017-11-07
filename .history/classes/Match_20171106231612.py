# DADSA - Assignment 1
# Reece Benson

class Match():
    player_one = None
    player_two = None
    player_one_score = None
    player_two_score = None
    
    def __init__(self, matchData = None, _round = None):
        self.matchData = matchData
        self.matchRound = _round
        self.playerA = None
        self.playerB = None
        self.winnerSet = False

    def getName(self):
        return self.matchRound.getName()

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
            