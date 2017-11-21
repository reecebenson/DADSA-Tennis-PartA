# DADSA - Assignment 1
# Reece Benson

class Player():
    _id = None
    _name = None
    _gender = None
    _wins = None
    _score = None
    _points = None

    def __init__(self, _name, _gender, _id):
        self._id = _id
        self._name = _name
        self._gender = _gender
        self._wins = { }
        self._score = { }
        self._points = 0

    def __cmp__(self, other):
        if(self._points < other._points):
            return -1
        elif(self._points > other._points):
            return 1
        else:
            return 0

    # Comparison Overrides
    #def __eq__(self, other):
    #    return not self._points < other._points and not other._points < self._points

    def __ne__(self, other):
        return self._points < other._points or other._points < self._points

    def __gt__(self, other):
        return other._points < self._points

    def __ge__(self, other):
        return not self._points < other._points

    def __le__(self, other):
        return not other._points < self._points

    def name(self):
        return self._name

    def gender(self):
        return self._gender

    def wins(self, _tournament):
        # Add Tournament Name to wins
        if(_tournament not in self._wins):
            self._wins.update({ _tournament: 0 })

        # Return our wins count
        return self._wins[_tournament]

    def wins_increase(self, _tournament):
        # Return our increased wins count
        return self.wins_set(_tournament, self.wins(_tournament) + 1)

    def wins_set(self, _tournament, _wins):
        # Add Tournament Name to wins
        if(_tournament not in self._wins):
            self._wins.update({ _tournament: 0 })

        # Update Tournament wins
        self._wins[_tournament] = _wins

        # Return our updated wins count
        return self._wins[_tournament]
    
    def score(self, _tournament, _round = None):
        # Add Tournament Name to score
        if(_tournament not in self._score):
            self._score.update({ _tournament: { } })

        # Are we viewing the score of a particular round
        if(_round != None):
            # Add Round to Tournament Name in Score
            if(_round not in self._score[_tournament]):
                self._score[_tournament].update({ _round: 0 })

            # Return our score count
            return self._score[_tournament][_round]
        else:
            # Return tournament scores
            return self._score[_tournament]

    def highest_score(self, _tournament):
        highest = max(self._score[_tournament], key=self._score[_tournament].get) 
        return { highest: self._score[_tournament][highest] }

    def score_set(self, _tournament, _round, _score_set):
        # Add Tournament Name to Score
        if(_tournament not in self._score):
            self._score.update({ _tournament: { } })

        # Add Round to Tournament in Score
        if(_round not in self._score[_tournament]):
            self._score[_tournament].update({ _round: 0 })

        # Update Tournament Score
        self._score[_tournament][_round] = _score_set

        # Return our updated score count
        return self._score[_tournament][_round]
    
    def points(self):
        return self._points

    def points_set(self, _points, append = False):
        if(append):
            self._points += _points
        else:
            self._points = _points
        return self._points