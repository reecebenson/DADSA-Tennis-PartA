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
from classes.File import File

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

    # Set our round mode via menu
    def set_round_mode(self, **mode):
        # Debug
        if(self.app.debug):
            print("Data passed to set_round_mode:")
            for key, value in mode.items():
                print("%s = %s" % (key, value))

        # Generate Data upto Round X
        if(mode['type'] == "empty"):
            self.round_mode[mode['season']] = partial(self.load_empty_rounds, mode['season'])
            Builder.close_menu()
        elif(mode['type'] == "generate"):
            self.round_mode[mode['season']] = partial(self.generate_rounds, mode['season'], 0, mode['rnd'])
            Builder.close_menu()
        elif(mode['type'] == "load"):
            self.round_mode[mode['season']] = partial(self.load_previous_rounds, mode['season'])
            Builder.close_menu()

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

        # Build Our Menu
        Builder.init(self.app, "How would you like to load the data for '{0}'?".format(season.name()))

        # Add Menus
        Builder.add_menu("main", "Empty Round Data", "empty_data")
        Builder.add_info("empty_data", "This will clear round data in 'seasons.json'.")
        Builder.add_menu("main", "Generate New Data", "gen_data")
        Builder.add_info("gen_data", "Generate new round data upto a specific round, this data is stored if the tournament saving flag is True")
        Builder.add_menu("main", "Load Previous Data", "load_data")
        Builder.add_info("load_data", "Loads previously saved round data from 'seasons.json'")

        # Add Functionality
        ## ROUNDS
        for r in range(1, (season.settings()["round_count"] + 1)):
            Builder.add_menu("gen_data", "Generate to Round {0}".format(r), "gen_data_{0}".format(r))
            Builder.add_func("gen_data", "gen_data_{0}".format(r), partial(self.set_round_mode, season=seasonId, type="generate", rnd=r))

        ## PREV DATA
        Builder.add_func("main", "empty_data", partial(self.set_round_mode, season=seasonId, type="empty"))
        Builder.add_func("main", "load_data", partial(self.set_round_mode, season=seasonId, type="load"))

        # Show Menu
        Builder.show_current_menu()

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
            tournament.set_season(season)
            tournament.set_prize_money([tournament_json['prize_money'][money] for money in tournament_json['prize_money']])
            tournament.set_difficulty(float(tournament_json['_difficulty']))
            tournament.set_file_saving(bool(tournament_json['_file_saving']))

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

    # Load empty rounds
    def load_empty_rounds(self, seasonId):
        # Get our Season Object
        season = self.get_season(seasonId)

        # Clear our rounds data
        for tn in season.tournaments():
            t = season.tournament(tn)
            t._rounds_raw = { }

            # Set our write to file flag to 'True' as we're (expected to) input rounds
            if(not t.file_saving()):
                t.toggle_file_saving(None)
            t.save_rounds()

    # Load round data from previous instance
    def load_previous_rounds(self, seasonId):
        # Get our Season Object
        season = self.get_season(seasonId)
        players = season.players()
        raw_json = season._j_data

        # Check that we have tournament data
        if(not "tournaments" in raw_json):
            raise("There are no tournaments within 'seasons.json'")

        # Check if the season has previous round data (through raw JSON)
        for tournament_name in raw_json['tournaments']:
            # Get our Tournament Object
            tournament = season.tournament(tournament_name)
            r_error_found = False
            error_found = False
            prev_round = { }

            # Check our rounds stored within the JSON data
            if("rounds" in raw_json['tournaments'][tournament_name]):
                # Load data in
                for rnd in raw_json['tournaments'][tournament_name]['rounds']:
                    r_path = raw_json['tournaments'][tournament_name]['rounds'][rnd]

                    for gdr in r_path:
                        # Check if we had a previous round
                        if(gdr not in prev_round):
                            prev_round.update({ gdr: None })

                        rg_path = r_path[gdr]

                        # Check if we have a round to take data from
                        match_cap = (len(players[gdr]) // 2) if (prev_round[gdr] == None) else (len(prev_round[gdr].winners()) // 2)

                        # Create our Round
                        round_cap = season.settings()[gdr.lower() + "_cap"] or 3
                        _r = Round.Round(self.app, gdr, rnd, tournament, match_cap)
                        _r.set_previous_round(prev_round[gdr])
                        _r.set_cap(round_cap)

                        # Add our Matches
                        for match in rg_path:
                            plyr_one = None
                            plyr_two = None

                            for i, plyr in enumerate(match, 0):
                                if(i == 0):
                                    plyr_one = [plyr, match[plyr]]
                                elif(i == 1):
                                    plyr_two = [plyr, match[plyr]]
                                else:
                                    break

                            # Setup our Match
                            _m = Match.Match(_r, season.player(gdr, plyr_one[0]), season.player(gdr, plyr_two[0]), plyr_one[1], plyr_two[1])

                            # Check if errors occurred, if they have - we want to update our file to fix these issues
                            m_error = True if _m.validate() > 0 else False
                            if(m_error):
                                error_found = True

                            # Add our Match to our round
                            _r.add_match(_m)
                        tournament.add_round(gdr, _r)

                        # Check if errors occurred, if they have - we want to update our file to fix these issues
                        r_error = True if _r.validate() > 0 else False
                        if(r_error):
                            r_error_found = True
                
                    # Set our previous round
                    if(gdr in prev_round):
                        prev_round[gdr] = _r

                # If errors have occurred, update file with fixes
                if(error_found or r_error_found):
                    self.handle_save_rounds(tournament)

            # Update Raw Rounds
            tournament.update_rounds_raw()

    # Generate our rounds from our player list from scratch
    def generate_rounds(self, seasonId, minRoundId, maxRoundId):
        # Write our new data to memory
        season = self.get_season(seasonId)
        players = season.players()

        # For each tournament, generate rounds
        for tournament_name in season.tournaments():
            # Get our tournament object
            tournament = season.tournament(tournament_name)

            # Generate our rounds
            for gender in players:
                for r in range(0, season.settings()["round_count"]):
                    # Define Round Variables
                    r_name = "round_" + str(r + 1)

                    # Make sure we're not generating over our requested generation amount
                    if    (r <  minRoundId): continue
                    elif  (r >= maxRoundId): break
                    else:                    pass

                    # Default Values
                    round_cap = 3

                    # Data to Check
                    prev_r = tournament.round(gender, "round_" + str(r))

                    # Check if we have a round to take data from
                    match_cap = (len(players[gender]) // 2) if (prev_r == None) else (len(prev_r.winners()) // 2)

                    # Do we have a Round Cap overrider for this gender?
                    round_cap = season.settings()[gender + "_cap"] or 3
                    _r = Round.Round(self.app, gender, r_name, tournament, match_cap)
                    _r.set_cap(round_cap)

                    # Check if we have a round to take data from
                    rnd_players = [ ]
                    if(prev_r == None):
                        rnd_players = random.sample(players[gender], len(players[gender]))
                    else:
                        rnd_players = random.sample(prev_r.winners(), len(prev_r.winners()))
                        _r.set_previous_round(prev_r)

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
                    tournament.add_round(gender, _r)

                    # Debug
                    if(self.app.debug):
                        print("{} --- Round Added: [{}]".format([ w.name() for w in _r.winners() ], r_name))

                # Import our data into JSON format for saving reference
                for g in tournament.rounds():
                    for r_id, r in enumerate(tournament.rounds()[g], 1):
                        # Make sure our round exists within the raw data
                        if(not "round_{0}".format(r_id) in tournament._rounds_raw):
                            tournament._rounds_raw.update({ "round_{0}".format(r_id): { } })

                        # Make sure our gender exists within the raw data
                        if(not g in tournament._rounds_raw["round_{0}".format(r_id)]):
                            tournament._rounds_raw["round_{0}".format(r_id)].update({ g: [ ] })

                        # Insert our data
                        tournament._rounds_raw["round_{0}".format(r_id)][g] = [ { m.player_one()[0].name(): m.player_one()[1], m.player_two()[0].name(): m.player_two()[1] } for m in tournament.round(g, r).matches() ]
            
            # Save Tournament Rounds (if enabled)
            if(tournament.file_saving()):
                tournament.save_rounds()
        
        # Debug
        if(self.app.debug):
            print("[LOAD]: Generated {1} rounds for season: '{0}', minRound: {2}, maxRound: {3}".format(season.name(), season.settings()['round_count'], minRoundId, maxRoundId))

        # End of generate_rounds()

    def handle_save_rounds(self, tournament):
        # Import our data into JSON format for saving reference
        for g in tournament.rounds():
            for r_id, r in enumerate(tournament.rounds()[g], 1):
                # Make sure our round exists within the raw data
                if(not "round_{0}".format(r_id) in tournament._rounds_raw):
                    tournament._rounds_raw.update({ "round_{0}".format(r_id): { } })

                # Make sure our gender exists within the raw data
                if(not g in tournament._rounds_raw["round_{0}".format(r_id)]):
                    tournament._rounds_raw["round_{0}".format(r_id)].update({ g: [ ] })

                # Insert our data
                tournament._rounds_raw["round_{0}".format(r_id)][g] = [ { m.player_one()[0].name(): m.player_one()[1], m.player_two()[0].name(): m.player_two()[1] } for m in tournament.round(g, r).matches() ]
    
        # Save Tournament Rounds (if enabled)
        if(tournament.file_saving()):
            tournament.save_rounds()

    def generate_round(self, seasonId, tournamentName, roundId, genderName):
        # Get our Season Object
        season = self.get_season(seasonId)
        players = season.players()

        # Ensure we have a valid Season object
        if(season == None):
            return print("Invalid Season ID: {}".format(seasonId))

        # Get our Tournament Object
        tournament = season.tournament(tournamentName)

        # Ensure we have a valid Tournament object
        if(tournament == None):
            return print("Invalid Tournament Name: {}".format(tournamentName))

        # Ensure we have valid round data
        previous_round = tournament.round(genderName, "round_{}".format(roundId - 1))
        if(previous_round == None and not (roundId - 1) == 0):
            return print("You can only generate this round when the rounds before Round {0} for {1}, {2} have been generated or manually inputed.".format(roundId, genderName.title(), tournamentName))

        # Start Generation of Round
        if(previous_round == None):
            rand_players = random.sample(players[genderName], len(players[genderName]))
        else:
            rand_players = random.sample(previous_round.winners(), len(previous_round.winners()))
            
        # Check if we have a round to take data from
        match_cap = (len(players[genderName]) // 2) if (previous_round == None) else (len(previous_round.winners()) // 2)

        # Generate our matches from the data we have
        round_cap = season.settings()[genderName + "_cap"] or 3
        _r = Round.Round(self.app, genderName, "round_{0}".format(roundId), tournament, match_cap)
        _r.set_previous_round(previous_round)
        _r.set_cap(round_cap)
        for w in range(len(rand_players) // 2):
            # Define our players
            p_one = rand_players[w * 2]
            p_two = rand_players[(w * 2) + 1]

            # Generate some scores
            p_one_score = random.randint(0, round_cap - 1)
            p_two_score = random.randint(0, round_cap - 1)

            # Make a random player the winner
            who = random.randint(0, 1)
            if(who == 0):   p_one_score = round_cap
            else:           p_two_score = round_cap

            # Add the match
            _r.add_match(Match.Match(_r, p_one, p_two, p_one_score, p_two_score))

        # Add our round to the tournament
        tournament.add_round(genderName, _r)
        
        # Save Data
        self.handle_save_rounds(tournament)
        return True

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