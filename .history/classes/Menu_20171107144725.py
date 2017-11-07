# DADSA - Assignment 1
# Reece Benson

from os import system as call
from collections import OrderedDict

class Menu():
    # Define the variables we will be using
    _app = None
    _menu = None
    _current_menu = 0

    def __init__(self, app):
        # Set our Application
        self._app = app

    def load(self):
        # Define our Menu
        self._menu = OrderedDict()

        # Main Menu
        self._menu["main"] = OrderedDict([("New Season", "new_season"), ("Load Season", "load_season")])

        # New Season Menu
        self._menu["new_season"] = OrderedDict([("Players", "ns_players"), ("Tournaments", "ns_tournaments"), ("Prize Money", "ns_prizemoney"), ("Difficulty", "ns_difficulty")])

        # Load Season Menu
        self._menu["load_season"] = OrderedDict()

        # Append our Seasons to the "Load Season" Menu
        for seasonId in self._app.handler.get_seasons():
            season = self._app.handler.get_season(seasonId)
            self._menu["load_season"].update({ season.name(): "load_season_"+str(seasonId) })

        # Display our Menu
        self.display()

    def display(self, index = None):
        # Clear our terminal window
        call("cls")

        # Define our variables
        cur_count = 0
        menu_item = self.get_menu(index or self.get_current_menu_index())

        # Menu Title, set tree
        tree = "(current: " + self.get_menu_name(self.get_current_menu_index()) + ")"
        print("Please select an option: {}".format(tree))

        menu_counter = 0
        for m in self._menu[menu_item]:
            # Increase our Counter
            menu_counter += 1

            # Is the Menu Item a Function?
            m_type = None
            if(callable(m)):    m_type = ""
            else:               m_type = "->"

            # Print our Menu Item
            print("{0}. {1} {2}".format(menu_counter, m, m_type))

        # Get User Input
        self.get_input()

    def get_current_menu_index(self):
        return self._current_menu

    def set_current_menu_index(self, new_index):
        self._current_menu = new_index

    def get_menu_name(self, index):
        return [ (v) for k,v in enumerate(self._menu) if(k == index) ][0]

    def get_menu(self, index):
        menu_item = self.get_menu_name(index)
        return menu_item

    def get_input(self):
        # Wrap this in a try/except to validate any errors with input
        try:
            # Get users input
            resp = input('>>> ')

            # Validate some set input calls
            if(resp == "exit"):
                raise KeyboardInterrupt
            elif(resp == ""):
                return self.display()
            
            self.set_current_menu_index(int(resp))
            self.display()
        except KeyboardInterrupt:
            self._app.exit()

    def load_action(self, menu_id):
        #TODO: Load Action from Menu_ID
        print("Load Action")