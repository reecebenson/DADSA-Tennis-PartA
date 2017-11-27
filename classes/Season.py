# DADSA - Assignment 1
# Reece Benson

from classes import Player
from classes import Round
from classes.File import File
from os import system as call

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
        self._settings = j_data['settings'] or None

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
                ret += "      {0}".format(" — ".join([ "#{0}: £{1:,}".format(i, int(t)) for i, t in enumerate(tournament.prize_money(), 1) ])) + "\n\n"
        elif(detail == "players"):
            if(extra == None):
                ret += "Error! Please define a gender."
            else:
                for i, player in enumerate(self.players()[extra], 1):
                    ret += "{0}. '{1}'\n".format(i, player.name())
        else:
            ret += "An unknown error has been handled..."
        return ret

    def tournaments(self):
        return self._tournaments

    def tournament(self, name):
        if(name in self.tournaments()):
            return self._tournaments[name]
        else:
            return None

    def add_tournament(self, name, tournament):
        # Add our tournament to our list
        self._tournaments.update({ name: tournament })
        
        # Add this tournament to all of our players scores
        for gdr in self.players():
            for p in self.players()[gdr]:
                p._score.update({ name: { } })

        # Debug
        if(self._app.debug):
            print("[LOAD]: Loaded Tournament '{0}' for '{1}'".format(name, self.name()))

        return self.tournament(name)

    def add_gender(self, name, cap):
        # Update Memory
        self._players.update({ name: [ ] })
        self._rounds.update({ name: [ ] })
        self._j_data['settings'].update({ name + "_cap": cap })

        # Update Files
        File.add_gender(self.name(), name, cap)

    def player(self, gender, name):
        if(gender in self.players()):
            for plyr in self.players()[gender]:
                if(plyr.name() == name):
                    return plyr
        return None

    def players(self):
        return self._players

    def add_player(self, name, gender):
        if(not gender in self.players()):
            self._players[gender] = [ ]
            self._rounds[gender] = [ ]

        # Append our Players to their specific gender category
        self._players[gender].append(Player.Player(name, gender, len(self.players()[gender])))

    def overall_view(self):
        ## Menu Selection
        available_tournaments = [ tn for tn in self.tournaments() ]
        selected_tournaments = [ ]
        all_selected = False

        # Handling
        error = False
        error_msg = ""

        ## Show Options
        while(not all_selected):
            ## Clear Terminal
            call("cls")

            # Show Error
            if(error):
                print("\nError:\n{}\n".format(error_msg))
                error = False

            print("Select tournaments you would like to migrate together:")
            for i, tn in enumerate(self.tournaments(), 1):
                print("{0}. {1} ({2})".format(i, tn, ("Selected" if tn in selected_tournaments else "Not Selected")))

            # Print Final
            if(len(selected_tournaments) > 0):
                print("\n{0}. View Overall Leaderboard for {1}".format(i + 1, (", ".join(selected_tournaments) if len(selected_tournaments) != 0 else "[None Selected]")))

            # Debug
            resp = input(">>> ")
            if(resp.isdigit()):
                got = int(resp)
                if(got >= 1 and got <= len(self.tournaments()) + (1 if(len(selected_tournaments) > 0) else 0)):
                    # Check if we're trying to view overall
                    if(got == len(available_tournaments) + 1):
                        all_selected = True
                        break
                    else:
                        # Toggle state of selected tournament
                        if(available_tournaments[got-1] in selected_tournaments):
                            del selected_tournaments[selected_tournaments.index(available_tournaments[got-1])]
                        else:
                            selected_tournaments.append(available_tournaments[got-1])
                else:
                    error = True
                    error_msg = "Please input a valid option"
            else:
                error = True
                error_msg = "Please input a valid option"

        ## Display all leaderboard data merged from selected tournaments
        print("Selected Tournaments: {}".format(", ".join(selected_tournaments)))
        