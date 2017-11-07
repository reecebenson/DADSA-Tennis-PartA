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

    # A method which exits the program after the user has pressed the Return key
    def exit(self):
        input(">>> Press <Return> to terminate the program")
        exit()

App()