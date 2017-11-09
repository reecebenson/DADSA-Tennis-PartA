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

    def emulate(self, season):
        # Start the emulation of our tournament (? from where we left off)
        # Get our Round Genders
        for i, gdr in enumerate(season.rounds(), 1):
            # Get our Rounds
            for r, rnd in enumerate(season.rounds()[gdr], 1):
                self.emulate_round(season, gdr, rnd)
                print(">>>>>>>>>>>>>>>> END OF ROUND")

    def emulate_round(self, season = None, gdr = None, rnd = None):
        # Get our Matches
        for m, match in enumerate(season.round(gdr, rnd).matches(), 1):
            print(match.versuses(True))

    def display(self, detail):
        # Set our header text
        ret = "Details about '{0}':".format(self.name()) + "\n"
        ret += "—————————————————————————————————————————————————————————" + "\n"
        
        # What detail are we handling?
        if(detail == "difficulty"):
            # Add difficulty string to the return string
            ret += "The difficulty multiplier for this tournament has been set as: {0}".format(self.difficulty()) + "\n"
        elif(detail == "prize_money"):
            ret += "Prize Money:" + "\n"
            ret += "{0}".format("\n".join([ "  #{0}: £{1:,}".format(i, int(t)) for i, t in enumerate(self.prize_money(), 1) ])) + "\n"
        elif(detail == "leaderboard"):
            ret += "leaderboard data"
        else:
            ret = "An unknown error has been handled..."
        return ret