# DADSA - Assignment 1
# Reece Benson

from functools import partial
from classes.File import File
from classes.Menu import Builder
from classes.QuickSort import quick_sort as sort

class Tournament():
    _app = None
    _name = None
    _season = None
    _rounds = None
    _rounds_raw = None
    _prize_money = None
    _difficulty = None
    _file_saving = None

    def __init__(self, app, name):
        # Set our Application
        self._app = app

        # Set our variables
        self._name = name
        self._rounds = { }
        self._rounds_raw = { }
        self._file_saving = False

    def name(self):
        return self._name

    def file_saving(self):
        return self._file_saving

    def set_file_saving(self, value):
        self._file_saving = value
        return self.file_saving()

    def save_rounds(self):
        return File.update_tournament_rounds(self.season().name(), self.name(), self._rounds_raw)

    def toggle_file_saving(self, menu_ref):
        # Update State
        self._file_saving = not self._file_saving

        # Update File Settings
        File.update_file_saving(self.season().name(), self.name(), self.file_saving())

        # Update Round Data within 'seasons.json'
        if(self.file_saving()):
            self.save_rounds()
        
        # Update Menu item
        if(menu_ref != None):
            Builder.add_menu(menu_ref, "{0} Saving".format("Disable" if self.file_saving() else "Enable"), "{0}_{1}".format(menu_ref, "fs"))

        # Skip over monitor_input halt
        return "SKIP"

    def season(self):
        return self._season

    def set_season(self, season):
        self._season = season
        return self.season()

    def rounds(self):
        return self._rounds

    def round(self, gender, rnd_name):
        if(gender in self.rounds()):
            if(rnd_name in self.rounds()[gender]):
                return self.rounds()[gender][rnd_name]
            else:
                return None
        else:
            return None

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

    def generate_round(self, gender, round_id, flag = None):
        # Generate specific round
        updated = self._app.handler.generate_round(self.season().name(), self.name(), round_id, gender)

        # Reload Menu
        if(updated and flag != "LOAD"):
            Builder.reload_menu()
            print("Successfully updated Round {0} for the {1} Gender on Tournament {2}.".format(round_id, gender.title(), self.name()))
        return None

    def input_round(self, gender, round_id, flag = None):
        # Generate specific round
        updated = self._app.handler.input_round(self.season().name(), self.name(), round_id, gender)

        # Reload Menu
        if(updated and flag != "LOAD"):
            Builder.reload_menu()
            print("Successfully inputted Round {0} for the {1} Gender on Tournament {2}.".format(round_id, gender.title(), self.name()))
        return None

    def edit_round(self, gender, round_id):
        # Check Round exists
        if(not self.round(gender, "round_{}".format(round_id))):
            return None

        # Header
        print("Editing {3} - {0} Round {1} - {2} matches exist\n".format(
                                                            gender.title(),
                                                            round_id,
                                                            len(self.round(gender, "round_{}".format(round_id)).matches()),
                                                            self.name()
                                                            ))

        # Count the changes made
        changes_made = 0

        for m in self.round(gender, "round_{}".format(round_id)).matches():
            shouldEdit = input("Would you like to edit [{1}] '{0}'? [y/N]: ".format(m.versuses(True), m.id())) or "n"

            if(shouldEdit.lower() == "y"):
                # Flag for changes in this match
                match_winner = m.winner()[0].name()
                match_changes = False
                match_cap = m.round().cap()

                # Player One Score
                plyr_one_score = input("Enter the Score for {0} (default: {1}): ".format(m.player_one()[0].name(), m.player_one()[1])) or str(m.player_one()[1])

                # Check if our score is different
                if(plyr_one_score.isdigit() and int(plyr_one_score) != m.player_one()[1]):
                    match_changes = True
                    changes_made += 1
                    m._player_one_score = int(plyr_one_score)

                # Player Two Score
                plyr_two_score = input("Enter the Score for {0} (default: {1}): ".format(m.player_two()[0].name(), m.player_two()[1])) or str(m.player_two()[1])
                if(plyr_two_score.isdigit() and int(plyr_two_score) != m.player_two()[1]):
                    match_changes = True
                    changes_made += 1
                    m._player_two_score = int(plyr_two_score)

                # Validate the match data
                m.validate()

                # Check if changes have been made
                if(match_changes):
                    # Check for winner change
                    if(match_winner != m.winner()[0].name()):
                        deleted_rounds = ", ".join([ r for r in self.rounds()[gender] if(self.round(gender, r).id() > round_id) ])
                        print("A new winner has been selected for this match, causing the deletion of the following rounds: {0}".format(deleted_rounds if deleted_rounds != "" else "< none >"))

                        # Delete rounds
                        for r in self.rounds()[gender].copy():
                            if(self.round(gender, r).id() > round_id):
                                # Update rounds_raw
                                self.delete_round(gender, r)
                    
                    # Update raw match data
                    self._rounds_raw["round_{}".format(round_id)][gender][m.id()].update({ m.player_one()[0].name(): m.player_one()[1], m.player_two()[0].name(): m.player_two()[1] })

                    # Save file
                    self.save_rounds()

                    # Debug
                    print("Match [{0}] has been updated successfully -> [{1}]\n".format(m.id(), m.versuses(True)))
                else:
                    print("No changes were made to Match [{0}] -> {0}\n".format(m.id(), m.versuses(True)))

        # Force a Menu Rebuild
        Builder.reload_menu()

        return None

    def clear_round(self, gender, round_id):
        # Verification
        verif = input("Are you sure you want to clear the following rounds [y/N]?\n{0}\n>>> ".format(", ".join([ r for r in self.rounds()[gender] if(self.round(gender, r).id() >= round_id) ]))) or "n"

        if(verif.lower() == "y"):
            # Delete rounds
            for r in self.rounds()[gender].copy():
                if(self.round(gender, r).id() >= round_id):
                    # Update rounds_raw
                    self.delete_round(gender, r)

                    # Output
                    print("Deleted Round: {0} -> {1} -> {2}".format(self.name(), gender, "Round "+str(r[-1:])))

            # Save file
            self.save_rounds()
        else:
            print("Cancelled ")

        # Force a Menu Rebuild
        Builder.reload_menu()
        return None

    def delete_round(self, g, r_id):
        # Check if our round exists
        if(not r_id in self._rounds_raw):
            return None

        # Check if our round gender exists
        if(not g in self._rounds_raw[r_id]):
            return None

        # Delete our round raw data
        self._rounds_raw[r_id].pop(g)

        # Update self variables
        self._rounds[g].pop(r_id)

        # Clean up
        if(len(self._rounds_raw[r_id]) == 0):
            self._rounds_raw.pop(r_id)

        # Done!
        return True

    def update_rounds_raw(self):
        # Import our data into JSON format for saving reference
        for g in self.rounds():
            for r_id, r in enumerate(self.rounds()[g], 1):
                # Make sure our round exists within the raw data
                if(not "round_{0}".format(r_id) in self._rounds_raw):
                    self._rounds_raw.update({ "round_{0}".format(r_id): { } })

                # Make sure our gender exists within the raw data
                if(not g in self._rounds_raw["round_{0}".format(r_id)]):
                    self._rounds_raw["round_{0}".format(r_id)].update({ g: [ ] })

                # Insert our data
                self._rounds_raw["round_{0}".format(r_id)][g] = [ { m.player_one()[0].name(): m.player_one()[1], m.player_two()[0].name(): m.player_two()[1] } for m in self.round(g, r).matches() ]
    
        return True

    def prize_money(self):
        return self._prize_money

    def set_prize_money(self, prize_money):
        self._prize_money = prize_money

    def difficulty(self):
        return self._difficulty

    def set_difficulty(self, difficulty):
        self._difficulty = difficulty

    def emulate(self):
        # Start the emulation of our tournament (? from where we left off)
        # Get our Round Genders
        for i, gdr in enumerate(self.rounds(), 1):
            # Get our Rounds
            for r, rnd in enumerate(self.rounds()[gdr], 1):
                self.emulate_round(gdr, rnd)
                print(">>>>>>>>>>>>>>>> END OF ROUND")

    def emulate_round(self, gdr = None, rnd = None):
        # Get our Matches
        for m, match in enumerate(self.round(gdr, rnd).matches(), 1):
            print(match.versuses(True))

    def display(self, detail, extra = None):
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
            if(extra == None):
                ret += "A gender must be specified."
            else:
                srt = sort(self.season().players()[extra])
                
                place = 1
                for i in reversed(range(len(srt))):
                    ret += ("#{0}: {1} — Points: {2}pts — {3}\n".format(place, srt[i].name(), srt[i].points() * self.difficulty(), "{0}: {1} score, {2} wins".format(self.name(), srt[i].score(self.name()), srt[i].wins(self.name()))))
                    place += 1
        else:
            ret = "An unknown error has been handled..."
        return ret