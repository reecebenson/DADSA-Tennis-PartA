# DADSA - Assignment 1
# Reece Benson

from os import system as call

class Round():
    _app = None
    _name = None
    _gender = None
    _matches = None
    _match_count = None
    _cap = 3

    def __init__(self, app=None, gender=None, name=None, match_cap=None):
        # Set our application
        self._app = app

        # Set our variables
        self._name = name
        self._gender = gender
        self._matches = [ ]
        self._match_cap = match_cap

    def name(self):
        return self._name

    def validate(self, error_count = 0):
        # Check if this round is statistically correct
        error = False
        
        # Check if the rounds are above the cap
        ## PLAYER ONE
        if(len(self.matches()) > self.match_cap()):
            # Error Occurred
            error = True
            error_count += 1

            # Print out the match for the user to see and reference to
            call("cls")
            print("Match Cap: {}, current match count: {}".format(self.match_cap(), len(self.matches())))

            print("CHECK MATCHES, NON-WINNERS IN PREV ROUND ETC.")
            new_score = input(">>> ")
            if(new_score.isdigit()):
                new_score = int(new_score)
                if(new_score >= 0 and new_score <= cap):
                    self._player_one_score = new_score
                else:
                    return self.validate(error_count)
            else:
                return self.validate(error_count)
        
        # Check if we're done (aggressive recursion)
        if(error):
            return self.validate(error_count)
        else:
            return error_count

    def gender(self):
        return self._gender

    def match_cap(self):
        return self._match_cap

    def set_match_cap(self, cap):
        self._match_cap = cap
        return self.match_cap()

    def cap(self):
        return self._cap

    def set_cap(self, cap):
        self._cap = cap
        return self.cap()

    def add_match(self, match):
        self._matches.append(match)

    def matches(self):
        return self._matches

    def match_count(self):
        return len(self.matches())

    def get_rank(self):
        return "n/a"

    def winners(self):
        _winners = [ w.winner()[0] for w in self.matches() ]
        return _winners