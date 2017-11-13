# DADSA - Assignment 1
# Reece Benson

import json
import random
from os import system as call
from functools import partial
from math import ceil, floor
from classes import Player
from classes import Season
from classes import Tournament
from classes import Round
from classes import Match
from classes.Menu import Builder

class Handler():
    # Define the variables we will be using
    app = None
    ranking_points = None
    player_count = None
    round_mode = None
    seasons = { }

    def __init__(self, _app):
        if(_app.debug):
            print("[LOAD]: Loaded Handler!")

        # Define our Application within this Handler class
        self.app = _app

    # Used to load all data into memory
    def load(self):
        # Define our Round Mode as a Dictionary
        self.round_mode = { }

        # This function will create our seasons
        self.load_seasons()
        self.load_ranking_points()

    # Used to load seasons into memory
    def load_seasons(self):
        with open('./data/seasons.json') as tData:
            data = json.load(tData)

            for season in data:
                # If the season does not yet exist, create it
                if(not season in self.get_seasons()):
                    self.seasons.update({ season: Season.Season(self.app, season, data[season]) })

                    # Check how the user would like to load data
                    _season = self.get_season(season)
                    self.load_rounds(season)
                    self.load_tournaments(season)
                    self.load_players(season)

                    # Execute the round mode (gen/load/overwrite)
                    if(season in self.round_mode):
                        if(callable(self.round_mode[season])):
                            self.round_mode[season]()
                            self.seasons[season]._j_data['settings'].update({ "loaded": True })
                        else:
                            # Let's go back to loading rounds
                            self.load_rounds(season, True, "The option you selected is unavailable.")

    # Load our rounds for each season
    def load_rounds(self, seasonId, error = False, errorMsg = None):
        # Get our Season Object
        season = self.get_season(seasonId)

        # Clear Terminal
        call("cls")

        # Was there an error?
        if(error):
            if(errorMsg != None):
                print("\nError:\n{0}\n".format(errorMsg))
            else:
                print("\nError:\nThere was an error performing your request.\n")

        # Question our user on how they would like to load data
        print("How would you like to load the data for '{0}'?".format(season.name()))
        print("1. Generate New Data")
        print("   -> This will override previous stored data!\n")
        print("2. Load Previous Data" if self.prev_rounds_exist(seasonId) else Builder.notAvailable("2. Load Previous Data"))
        print("   -> Import data from the `seasons.json` file\n")
        print("3. Manual Input Data")
        print("   -> Import data manually using the terminal window\n")

        try:
            resp = input(">>> ")
            if(resp.isdigit()):
                req = int(resp)
                if(req >= 1 and req <= 3):
                    if(req == 1):
                        # Generate Round Data
                        self.round_mode[seasonId] = partial(self.generate_rounds, seasonId)
                    elif(req == 2):
                        if(self.prev_rounds_exist(seasonId)):
                            # Load Data from previous terminal instance
                            self.round_mode[seasonId] = partial(self.load_previous_rounds, seasonId)
                        else:
                            self.load_rounds(seasonId, True, "That option is unavailable.")
                    elif(req == 3):
                        self.round_temp = { "genders": None, "players": None, "tournaments": None }
                        self.round_mode[seasonId] = partial(self.input_manual_rounds, seasonId)
                else:
                    self.load_rounds(seasonId, True)
            else:
                self.load_rounds(seasonId, True)
        except KeyboardInterrupt:
            self.app.exit()

    # Load our tournaments for each season
    def load_tournaments(self, seasonId):
        # Get our Season Object
        season = self.get_season(seasonId)
        
        # Grab Tournaments from raw JSON data stored in the Season
        for tournament_name in season._j_data['tournaments']:
            # Make sure that we're importing a tournament
            if("round" in tournament_name):
                continue

            tournament_json = season._j_data['tournaments'][tournament_name]

            # Create our Tournament
            tournament = Tournament.Tournament(self.app, tournament_name)
            tournament.set_prize_money([tournament_json[money] for money in tournament_json if(not "_difficulty" in money)])
            tournament.set_difficulty(float(tournament_json['_difficulty']))

            # Add our Tournament to our Season
            season.add_tournament(tournament_name, tournament)

    # Input manual scores
    def input_scores(self, seasonId, gender, roundId):
        # Get our Season Object
        season = self.get_season(seasonId)
        _round = season.round(gender, roundId)

        # Check if this round has any data
        print("blah blah {}, round {}, gender {}".format(seasonId, roundId, gender))

    # Start the manual input of data for the Season
    def input_manual_rounds(self, seasonId):
        # Get our Season Object
        season = self.get_season(seasonId)

        # Build our menu
        Builder.init(self.app, "[Editing '{0}'] Please select an option:".format(season.name()))
        Builder.add_menu("main", "Input Scores", "score_input")
        Builder.add_menu("main", "End Editing", "end_manual_rounds")
        Builder.add_menu("end_manual_rounds", "Stop Editing", "return")

        # Add our rounds per gender
        for gdr in season.players():
            # Add Menu Items
            Builder.add_menu("score_input", "{0} Rounds".format(gdr.title()), "score_input_{0}".format(gdr))

            # Add Gender Specific Menu Items
            for r in range(1, (season.settings()["round_count"] + 1)):
                # Display Round
                rnd = season.round(seasonId, r)
                Builder.add_menu("score_input_{0}".format(gdr), "Round {0} {1}".format(r, ("(No Previous Data)" if rnd == None else "")), "score_input_{0}_{1}".format(r, gdr))

                # Add menu functionality
                Builder.add_func("score_input", "score_input_{0}_{1}".format(r, gdr), partial(self.input_scores, seasonId, gdr, r))

        # Add Functionality
        Builder.add_func("end_manual_rounds", "return", None)

        # Display Menu
        Builder.show_current_menu()

    # Check if previous round data exists within the Season
    def prev_rounds_exist(self, seasonId):
        # Get our Season Object
        season = self.get_season(seasonId)
        raw_json = season._j_data

        # Check if the season has previous round data
        return ("rounds" in raw_json)
        
    # Load round data from previous instance
    def load_previous_rounds(self, seasonId):
        # Get our Season Object
        season = self.get_season(seasonId)
        raw_json = season._j_data

        # Check if the season has previous round data
        if(self.prev_rounds_exist(seasonId)):
            return
        
        # Round exists, lets import our data to our season
        input("data exists, yay")

    # Generate our rounds from our player list from scratch
    def generate_rounds(self, seasonId):
        # Write our new data to memory
        season = self.get_season(seasonId)
        players = season.players()

        # Generate our rounds
        for gender in players:
            for r in range(0, season.settings()["round_count"]):
                # Default Values
                round_cap = 3

                # Do we have a Round Cap overrider for this gender?
                if(gender + "_cap" in season.settings()):
                    round_cap = season.settings()[gender + "_cap"]

                # Define Round Variables
                r_id = (r + 1)
                r_name = "round_" + str(r_id)
                _r = Round.Round(self.app, gender, r_name)

                # Data to Check
                prev_r = season.round(gender, "round_" + str(r))

                # Check if we have a round to take data from
                rnd_players = [ ]
                if(prev_r == None):
                    rnd_players = random.sample(players[gender], len(players[gender]))
                else:
                    rnd_players = random.sample(prev_r.winners(), len(prev_r.winners()))

                # Generate our matches from the data we have
                for w in range(len(rnd_players) // 2):
                    # Define our players
                    p_one = rnd_players[w * 2]
                    p_two = rnd_players[(w * 2) + 1]

                    # Generate some scores
                    p_one_score = random.randint(0, round_cap - 1)
                    p_two_score = random.randint(0, round_cap - 1)

                    # Make a random player the winner
                    who = random.randint(0, 1)
                    if(who == 0):   p_one_score = round_cap
                    else:           p_two_score = round_cap

                    # Add the match
                    _r.add_match(Match.Match(_r, p_one, p_two, p_one_score, p_two_score))

                # Add our round to our season
                season.add_round(gender, _r)
        
        # Debug
        if(self.app.debug):
            print("[LOAD]: Generated {1} rounds for season: '{0}'".format(season.name(), season.settings()['round_count']))

        # Write to Rounds
        
        # End of generate_rounds()

    # Used to load prize money
    def load_ranking_points(self):
        with open('./data/rankingPoints.json') as tData:
            data = json.load(tData)

            # Fallback on a non-existant occurrence
            if(self.player_count == None):
                self.player_count = 100

            # Make our ranking_points a dictionary
            if(self.ranking_points == None):
                self.ranking_points = { }

            # Set the prize money to the actual rank and points received
            self.ranking_points  = [ pts for pts in data for rank in data[pts] ]

            # We want to set the prize money for all indexes possible via the player
            self.ranking_points += [ 0 ] * ( self.player_count - len(self.ranking_points))

    # Used to load players from all seasons into memory
    def load_players(self, seasonId):
        # Set our player (in gender) count
        self.player_count = 0

        with open('./data/players.json') as tData:
            data = json.load(tData)

            # Players are classed within Seasons
            for season in data:
                # If the season does not yet exist, ignore this input
                if((not season in self.get_seasons()) or (season != seasonId)):
                    continue

                # Players are then stored within Gender classifications
                for gender in data[season]:
                    if(not gender in self.get_season(season).players()):
                        self.get_season(season).players()[gender] = [ ]

                    # Append our player in the season, within the gender
                    for player in data[season][gender]:
                        #TODO: Change to using Player class
                        self.get_season(season).add_player(player, gender)

                        # Update our player count
                        if(len(self.get_season(season).players()[gender]) > self.player_count):
                            self.player_count = len(self.get_season(season).players()[gender])

    def get_round_status(self):

        pass

    def write_round(self):

        pass

    def get_seasons(self):
        return self.seasons

    def get_season(self, season_id):
        if(season_id in self.seasons):
            return self.seasons[season_id]
        else:
            return None