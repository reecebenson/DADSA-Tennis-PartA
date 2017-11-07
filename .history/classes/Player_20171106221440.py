# DADSA - Assignment 1
# Reece Benson

class Player():
    _id = None
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
        if(self._points < other._points):
            return -1
        elif(self._points > other._points):
            return 1
        else:
            return 0

    # Comparison Overrides
    def __eq__(self, other):
        return not self._points < other._points and not other._points < self._points

    def __ne__(self, other):
        return self._points < other._points or other._points < self._points

    def __gt__(self, other):
        return other._points < self._points

    def __ge__(self, other):
        return not self._points < other._points

    def __le__(self, other):
        return not other._points < self._points

    def get_name(self):
        return self._name

    def get_gender(self):
        return self._gender

    def get_score(self, _match):
        return self._score[_match]

    def set_score(self, _match, _score):
        self.score[_match] = _score
        return self._score[_match]
    
    def get_points(self):
        return self._points

    def set_points(self, _points, append = False):
        if(append):
            self._points += _points
        else:
            self._points = _points
        return self._points