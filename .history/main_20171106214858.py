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
        players = self.handler.get_players("season_1")

        # Let's generate our random rounds from scratch
        round_data = {
            "male": [ { "_roundCap": 3 } ],
            "female": [ { "_roundCap": 2 } ]
        }

        print(round_data)
    
    # A method which exits the program after the user has pressed the Return key
    def exit(self):
        input(">>> Press <Return> to terminate the program")
        exit()

App()