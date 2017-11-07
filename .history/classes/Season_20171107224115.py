# DADSA - Assignment 1
# Reece Benson

from classes import Player
from classes import Round

class Season():
    _app = None
    _j_data = None
    _name = None
    _players = { }
    _tournaments = { }
    _rounds = { }
    _rounds_raw = { }
    _settings = { }

    def __init__(self, _app, name, j_data):
        # Set our application as a variable
        self._app = _app
        
        # Set our Season JSON Data in a variable
        self._j_data = j_data

        # Debug
        if(self._app.debug):
            print("[LOAD]: Loaded Season '{0}'".format(name))

        # Set variables
        self._name = name
        self._settings = j_data['settings']

    def name(self):
        return self._name

    def settings(self):
        return self._settings

    def display(self, detail, extra = None):
        # Set our header text
        ret = "Details about '{0}':".format(self.name()) + "\n"
        ret += "—————————————————————————————————————————————————————————" + "\n"
            
        # What detail are we handling?
        if(detail == "details"):
            # Add details to the return string
            ret += "There have been {0} genders defined within this season".format(len(self.players())) + "\n"
            for gdr in self.players():
                ret += " -> The gender '{0}' has {1} players stored within it:".format(gdr, len(self.players()[gdr])) + "\n"
                ret += " ALL: " + ", ".join([p.name() for p in self.players()[gdr] ]) + "\n"
            
            # Add settings
            ret += "\n" + "Settings for this season:" + "\n"
            for setting in self.settings():
                ret += " -> The setting '{0}' is set to '{1}'".format(setting, self.settings()[setting]) + "\n"

            # Show tournaments
            ret += "\n" + "Tournaments in this season:" + "\n"
            for tournament_name in self.tournaments():
                tournament = self.tournament(tournament_name)
                ret += " -> {0} — Difficulty: {1}".format(tournament_name, tournament.difficulty()) + "\n"
                ret += "    Prize Money:" + "\n"
                ret += "      {0}".format(", ".join([ "#{0}: £{1:,}".format(i, int(t)) for i, t in enumerate(tournament.prize_money(), 1) ])) + "\n"
        elif(detail == "players"):
            if(extra == None):
                ret += "Error! Please define a gender."
            else:
                for i, player in enumerate(self.players()[extra], 1):
                    ret += "{0}. '{1}'\n".format(i, player.name())
        else:
            ret += "An unknown error has been handled..."

        # Returning as a string, so if there was a GUI I could
        # append this to a Label instead of printing to console
        return ret

    def tournaments(self):
        return self._tournaments

    def tournament(self, name):
        if(name in self.tournaments()):
            return self._tournaments[name]
        else:
            return None

    def add_tournament(self, name, tournament):
        self._tournaments.update({ name: tournament })

        # Debug
        if(self._app.debug):
            print("[LOAD]: Loaded Tournament '{0}' for '{1}'".format(name, self.name()))

        return self.tournament(name)

    def players(self):
        return self._players

    def add_player(self, name, gender):
        if(not gender in self.players()):
            self._players[gender] = [ ]
            self._rounds[gender] = [ ]

        # Append our Players to their specific gender category
        self._players[gender].append(Player.Player(name, gender, len(self.players()[gender])))

    def round(self, gender, rnd_name):
        if(gender in self.rounds()):
            if(rnd_name in self.rounds()[gender]):
                return self.rounds()[gender][rnd_name]
            else:
                return None
        else:
            return None

    def rounds(self):
        return self._rounds

    def add_round(self, gender, _round):
        if(not gender in self.rounds()):
            self._rounds[gender] = { }

        self._rounds[gender].update({ _round.name(): _round })
        return self._rounds[gender][_round.name()]

    def set_rounds(self):
        for rnd in self._rounds_raw:
            for gdr in self._rounds_raw[rnd]:
                # If the Gender category doesn't exist within the rounds, create it
                if(not gdr in self._rounds):
                    self._rounds[gdr] = [ ]

                # Populate our dictionary with our match data
                for match in self._rounds_raw[rnd][gdr]:
                    _round._matches.append(match)

                # Append our Round
                self._rounds[gdr].append(_round)
