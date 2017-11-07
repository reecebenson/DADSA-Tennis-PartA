# DADSA - Assignment 1
# Reece Benson

import random
from classes import Menu as Menu
from classes import Handler as Handler

class App():
    # Define the variables we will be using
    debug = True
    handler = None

    # Define all of the properties we will need to use
    def __init__(self):
        # Load our handler
        self.handler = Handler.Handler(self)
        self.handler.load()

        # Generate rounds
        self.generate_rounds()

        # Hold the program
        self.exit()

    # Generate our rounds from our player list
    def generate_rounds(self):
        # Let's generate our random rounds from scratch
        round_data = { }

        # Write our new data to memory
        for seasonId in self.handler.get_seasons():
            season = self.handler.get_season(seasonId)
            players = season.players()

            # Generate our rounds
            for gender in players:
                # Default Round Cap
                round_cap = 3

                # Create our gendered rounds
                if(not gender in round_data):

                    # Do we have a Round Cap overrider for this gender?
                    if(gender + "_cap" in season.settings()):
                        roundCap = season.settings()[gender + "_cap"]
                    
                    # Update our round data
                    round_data.update({ gender: [ { "_roundCap": round_cap } ] })

                # Create our match data from players
                rnd_players = random.sample(players[gender], len(players[gender]))
                for i in range(int(len(rnd_players) / 2 )):
                    # Grab our versus players
                    p_one = rnd_players[i * 2]
                    p_two = rnd_players[(i * 2) + 1]

                    # Generate some scores
                    p_one_score = random.randint(0, round_cap - 1)
                    p_two_score = random.randint(0, round_cap - 1)

                    # Make a random player the winner
                    who = random.randint(0, 1)
                    if(who == 0):   p_one_score = round_cap
                    else:           p_two_score = round_cap

                    # Append our random data
                    round_data[gender].append({ p_one.name(): p_one_score, p_two.name(): p_two_score })

                
    
            # Set our Round Data to our season
            season.set_rounds_raw(round_data)
        
        # End of generate_rounds()

    # A method which exits the program after the user has pressed the Return key
    def exit(self):
        input(">>> Press <Return> to terminate the program")
        exit()

App()