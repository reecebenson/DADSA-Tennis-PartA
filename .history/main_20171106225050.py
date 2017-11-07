# DADSA - Assignment 1
# Reece Benson

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
                # Create our gendered rounds
                if(not gender in round_data):
                    # Default Round Cap
                    roundCap = 3 

                    # Do we have a Round Cap overrider for this gender?
                    if(gender + "_cap" in season.settings()):
                        roundCap = season.settings()[gender + "_cap"]
                    
                    # Update our round data
                    round_data.update({ gender: [ { "_roundCap": roundCap } ] })

                # Create our round data from players
                x = 0
                for i in range(len(players[gender]) / 2):
                    playerOne = players[gender][x]
                    playerTwo = players[gender][x + 1]
                    print("{0} vs {1} ".format(playerOne.name(), playerTwo.name()))
                    x += 2
    
        print(round_data)

    # A method which exits the program after the user has pressed the Return key
    def exit(self):
        input(">>> Press <Return> to terminate the program")
        exit()

App()