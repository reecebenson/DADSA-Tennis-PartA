# DADSA - Assignment 1
# Reece Benson

import json
import random
from classes import Player as Player
from classes import Season as Season
from classes import Tournament as Tournament
from classes import Round as Round
from classes import Match as Match

class Handler():
    # Define the variables we will be using
    app = None
    prize_money = None
    player_count = None
    seasons = { }

    def __init__(self, _app):
        if(_app.debug):
            print("[LOAD]: Loaded Handler!")

        # Define our Application within this Handler class
        self.app = _app

    # Used to load all data into memory
    def load(self):
        # This function will create our seasons and implement the genders & players
        self.load_seasons()
        self.load_players()
        self.load_prize_money()

        #TODO: Implement load_seasons()

    # Used to load seasons into memory
    def load_seasons(self):
        with open('./data/seasons.json') as tData:
            data = json.load(tData)

            for season in data:
                # If the season does not yet exist, create it
                if(not season in self.get_seasons()):
                    self.seasons.update({ season: Season.Season(self.app, season, data[season]) })

    # Generate our rounds from our player list from scratch
    def generate_rounds(self):
        # Write our new data to memory
        for seasonId in self.get_seasons():
            season = self.get_season(seasonId)
            players = season.players()

            # Our Round Data should be completely empty
            round_data = { }

            # Generate our rounds
            for gender in players:
                # Generate 'x' amount of rounds
                for r in range(1, season.settings()['round_count']):
                    # Default Values
                    round_name = "round_"+str(r)
                    round_cap = 3

                    # Create our gendered rounds
                    if(not gender in round_data):
                        # Do we have a Round Cap overrider for this gender?
                        if(gender + "_cap" in season.settings()):
                            roundCap = season.settings()[gender + "_cap"]
                        
                        # Update our round data
                        round_data.update({ round_name: { gender: [ ] } })

                    # Create our match data from players
                    rand_players = random.sample(players[gender], len(players[gender]))
                    for i in range(int((len(rand_players) / 2) / r)):
                        # Grab our versus players
                        p_one = rand_players[i * 2]
                        p_two = rand_players[(i * 2) + 1]

                        # Generate some scores
                        p_one_score = random.randint(0, round_cap - 1)
                        p_two_score = random.randint(0, round_cap - 1)

                        # Make a random player the winner
                        who = random.randint(0, 1)
                        if(who == 0):   p_one_score = round_cap
                        else:           p_two_score = round_cap

                        # Append our random data as a Match
                        #round_data[gender].append({ p_one.name(): p_one_score, p_two.name(): p_two_score })
                        round_data[round_name][gender].append(Match.Match(round_name, p_one, p_two, p_one_score, p_two_score))
    
                # Set our Round Data to our season
                season.set_rounds_raw(round_data)
            
            # Debug
            if(self.app.debug):
                print("[LOAD]: Generated {1} rounds for season: '{0}'".format(season.name(), season.settings()['round_count']))
                print(len(season.rounds()["male"]))
                for match in season.rounds()["male"]:
                    print(match.versuses(), match.round())
        
        # End of generate_rounds()

    # Used to load prize money
    def load_prize_money(self):
        with open('./data/rankingPoints.json') as tData:
            data = json.load(tData)

            # Fallback on a non-existant occurrence
            if(self.player_count == None):
                self.player_count = 100

            # Make our prize_money a dictionary
            if(self.prize_money == None):
                self.prize_money = { }

            # Set the prize money to the actual rank and points received
            self.prize_money  = [ pts for pts in data for rank in data[pts] ]

            # We want to set the prize money for all indexes possible via the player
            self.prize_money += [ 0 ] * ( self.player_count - len(self.prize_money))

    # Used to load players from all seasons into memory
    def load_players(self):
        # Set our player (in gender) count
        self.player_count = 0

        with open('./data/players.json') as tData:
            data = json.load(tData)

            # Players are classed within Seasons
            for season in data:
                # If the season does not yet exist, ignore this input
                if(not season in self.get_seasons()):
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

    def get_seasons(self):
        return self.seasons

    def get_season(self, season_id):
        if(season_id in self.seasons):
            return self.seasons[season_id]
        else:
            return None