# DADSA - Assignment 1
# Reece Benson
from classes import Handler as Handler
from classes import Player as Player
from classes import Season as Season
from classes import Tournament as Tournament
from classes import Round as Round
from classes import Match as Match

class App():
    # Define the variables we will be using
    handler = None

    # Define all of the properties we will need to use
    def __init__(self):
        # Load our handler
        self.handler = Handler.Handler()
        self.handler.loadPlayers()

        # Generate rounds

        # Hold the program
        self.exit()

    # Generate our rounds from our player list
    def generate_rounds(self):

    
    # A method which exits the program after the user has pressed the Return key
    def exit(self):
        input(">>> Press <Return> to terminate the program")
        exit()

App()