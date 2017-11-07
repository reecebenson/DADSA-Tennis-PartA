# DADSA - Assignment 1
# Reece Benson
from classes import Handler as Handler
from classes import Player as Player
from classes import Season as Season
from classes import Tournament as Tournament
from classes import Round as Round
from classes import Match as Match

class App():
    def __init__(self):
        handler = Handler.Handler()

        # Hold the program
        self.exit()
    
    # A method which exits the program after the user has pressed 
    def exit(self):
        input(">>> Press <Return> to terminate the program")
        exit()


App()