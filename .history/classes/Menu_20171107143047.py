# DADSA - Assignment 1
# Reece Benson

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

    def display(self):
        cur_count = 0
        m = self.get_menu(self.get_current_menu_index())
        
        """for i in m:
            # Is the Menu Item a Function?
            m_type = None
            if(callable(m[i])): m_type = ""
            else:               m_type = "->"
            
            cur_count += 1
            print("{0}. {1}".format(cur_count, i, m_type))"""

        # Get User Input
        self.get_input()

    def get_current_menu_index(self):
        return self._current_menu

    def get_menu_name(self, menu):
        return [ (v) for k,v in enumerate(self._menu) if(k == menu) ][0]

    def get_menu(self, menu):
        menu_name = self.get_menu_name(menu)

        for m in (range(i), self._menu[menu_name]):
            print(m)

    def get_input(self):
        resp = input(">>> ")
        self.get_menu(resp)

    def load_action(self, menu_id):
        #TODO: Load Action from Menu_ID
        print("Load Action")