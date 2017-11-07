# DADSA - Assignment 1
# Reece Benson

class Player():
    id = None
    _name = None
    _gender = None
    _score = None
    _points = None

    def __init__(self, _name, _gender, _id):
        self._id = _id
        self._name = _name
        self._gender = _gender
        self._score = { }
        self._points = 0

    def __cmp__(self, other):
        """Compare Override"""
        if(self.points < other.points):
            return -1
        elif(self.points > other.points):
            return 1
        else:
            return 0

    # Comparison Overrides
    def __eq__(self, other):
        return not self.points < other.points and not other.points < self.points

    def __ne__(self, other):
        return self.points < other.points or other.points < self.points

    def __gt__(self, other):
        return other.points < self.points

    def __ge__(self, other):
        return not self.points < other.points

    def __le__(self, other):
        return not other.points < self.points

    def getName(self):
        """Get the Name of this Player"""
        return self.name

    def getGender(self):
        """Get the Gender of this Player"""
        return self.gender

    def getScore(self, _match):
        """ Get the Score of this Player"""
        return self.score[_match]

    def setScore(self, _match, _score):
        """ Set the Score of this Player"""
        self.score[_match] = _score
        return self.score[_match]
    
    def getRankingPoints(self):
        """ Get the Ranking Points of this Player"""
        return self.points

    def setRankingPoints(self, _points, append = False):
        """ Set the Ranking Points of this Player"""
        if(append):
            self.points += _points
        else:
            self.points = _points
        return self.points

    def asTree(self):
        return ("[{2}] [ name: {0}, gender: {1}, points: {3} ]".format(self.getName(), self.getGender(), self.id, self.getRankingPoints()))