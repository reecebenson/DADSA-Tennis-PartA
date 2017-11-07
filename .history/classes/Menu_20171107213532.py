# DADSA - Assignment 1
# Reece Benson

from functools import partial
from os import system as call
from collections import OrderedDict

class Menu():
    # Define the variables we will be using
    _app = None
    _menu = None
    _current = [ "main" ]
    _current_menu = "main"
    just_called_back = False

    def __init__(self, app):
        # Set our Application
        self._app = app

    def load(self):
        # Define our Menu
        self._menu = { }

        # Create our Menu
        self._menu['main'] = { "new_season": "New Season", "load_season": "Load Season" }
        self._menu['back'] = lambda: self.go_back()
        self._menu['new_season'] = { "ns_players": "Players", "ns_tournaments": "Tournaments", "ns_prizemoney": "Prize Money", "ns_difficulty": "Difficulty", "back": "Back" }
        self._menu['ns_players'] = { "ns_viewplayers": "View Players", "ns_viewplayer": "View Player", "back": "Back" }
        self._menu['ns_tournaments'] = { "ns_viewtournaments": "Example Tournament 1", "back": "Back" }
        self._menu['ns_prizemoney'] = { "ns_setprizemoney": "Set Prize Money", "ns_viewprizemoney": "View Prize Money", "back": "Back" }
        self._menu['ns_difficulty'] = { "ns_setdifficulty": "Set Difficulty", "ns_viewdifficulty": "View Difficulty", "back": "Back" }
        self._menu['load_season'] = { }

        # Append our Seasons to the "Load Season" Menu
        for seasonId in self._app.handler.get_seasons():
            season = self._app.handler.get_season(seasonId)
            seasonVar = 'ls_'+str(seasonId)
            self._menu['load_season'].update({ seasonVar: season.name() })

            # Create our menu option for loading a season
            self._menu[seasonVar] = { seasonVar+"_select": "Select Tournament", seasonVar+"_players": "View Players", seasonVar+"_details": "View Details", "back": "Back" }

            # Create our menu options
            self._menu[seasonVar+"_select"] = { }
            self._menu[seasonVar+"_players"] = { }
            self._menu[seasonVar+"_details"] = lambda: print(season.display("details"))

            # Fill our menu options with extra options
            # > "Select Tournament"
            for tournament_name in season.tournaments():
                tournamentVar = seasonVar+"_select_"+tournament_name

                self._menu[seasonVar+"_select"].update({ tournamentVar: "Select {0}".format(tournament_name) })

                # Set our gender specifiers within the tournament
                self._menu[tournamentVar] = { }
                for gdr in season.rounds():
                    self._menu[tournamentVar].update({ tournamentVar+"_"+gdr: "View {0} Rounds".format(gdr) })

                    self._menu[tournamentVar+"_"+gdr] = { }
                    for r, rnd in enumerate(season.rounds()[gdr], 1):
                        self._menu[tournamentVar+"_"+gdr].update({ tournamentVar+"-"+gdr+"-"+rnd: "Round {0}".format(r) })
                        self._menu[tournamentVar+"-"+gdr+"-"+rnd] = partial(print, "\n".join([ "{0} — Winner: {1}    ".format(m.versuses(True), m.winner()[0].name()) for m in season.round(gdr, rnd).matches() ]))
                    self._menu[tournamentVar+"_"+gdr].update({ "back": "Back" })

                # Add tournament specific options
                self._menu[tournamentVar].update({ tournamentVar+"_difficulty": "View Difficulty", tournamentVar+"_prizemoney": "View Prize Money" })
                self._menu[tournamentVar+"_difficulty"] = partial(print, season.tournament(tournament_name).display("difficulty"))
                self._menu[tournamentVar+"_prizemoney"] = partial(print, season.tournament(tournament_name).display("prize_money"))

                # Add our back option
                self._menu[tournamentVar].update({ "back": "Back" })

            # > "View Players"
            for gdr in season.players():
                self._menu[seasonVar+"_players"].update({ seasonVar+"_players_"+gdr: "List {0}s".format(gdr) })
                self._menu[seasonVar+"_players_"+gdr] = lambda: print(season.display("players", gdr))

            # > Add the back options to each submenu
            self._menu[seasonVar+"_select"].update({ "back": "Back" })
            self._menu[seasonVar+"_players"].update({ "back": "Back" })
        self._menu["load_season"].update({ "back": "Back" })

        # Display our Menu
        self.display("main")

    def go_back(self):
        # Set our flag to true
        self.just_called_back = True

        # Pop off the last item of the list
        self._current.pop()

        # Set our current menu to the last element of the list
        self._current_menu = self._current[-1]

    def strike(self, text):
        result = ''
        for c in text:
            result = result + c + '\u0336'
        return result

    def display(self, index = None, error = None):
        # Clear our terminal window
        call("cls")

        # Define our variables
        cur_count = 0
        menu_item = self.get_menu(index or "main")

        # Error Handling
        if(error != None):
            print("\n", "Error!", error, "\n")

        # Menu Title, set tree
        print("Please select an option: ({})".format("/".join(self._current)))

        menu_counter = 0
        for m in menu_item:
            # Get our menu name
            menu_name = menu_item[m]

            # Increase our Counter
            menu_counter += 1

            # Check that the menu option is available
            if(m in self._menu):
                # Is the Menu Item a Function?
                m_type = None
                if(callable(self._menu[m])):
                    m_type = ""
                else:
                    m_type = "->"

                # Print our Menu Item
                print("{0}. {1} {2}".format(menu_counter, menu_name, m_type))
            else:
                print(self.strike("{0}. {1} [?]".format(menu_counter, menu_name)))

        # Get User Input
        self.get_input()

    def validate_menu(self, index):
        try:
            menu_name = [ (v) for k,v in enumerate(self._menu) if(k == index) ][0]
            return menu_name
        except IndexError:
            return None

    def get_menu(self, menu_name):
        # Check our Menu exists
        if(not menu_name in self._menu):
            return None
        else:
            return self._menu[menu_name]

    def menu_exists(self, index):
        # Find our indexed menu
        menu_item = self.get_menu(self._current_menu)

        menu_found = None
        menu_counter = 0
        for m in menu_item:
            # Get our menu name
            menu_name = menu_item[m]

            # Increase our Counter
            menu_counter += 1

            # Check that the menu option is available
            if(m in self._menu):
                # Has our menu been found?
                if(menu_counter == index):
                    # Check if it's a function or a submenu
                    if(callable(self._menu[m])):
                        # Call our function
                        menu_found = self._menu[m]
                    else:
                        menu_found = m
            else:
                menu_found = None
        return menu_found

    def get_input(self):
        # Wrap this in a try/except to validate any errors with input
        try:
            # Get users input
            resp = int(input('\n>>> '))

            # Validate some set input calls
            if(resp == "exit"):
                raise KeyboardInterrupt
            elif(resp == ""):
                return self.display(self._current_menu, "Please select a valid option!")
            
            # Validate input from current menu
            menu_selected = self.menu_exists(resp)
            if(menu_selected != None and callable(menu_selected) != True):
                print(menu_selected)
                self._current.append(menu_selected)
                self._current_menu = menu_selected
                self.display(menu_selected)
            elif(callable(menu_selected)):
                # Clear our screen
                call("cls")

                # Call our function
                menu_selected()

                # Hold the user so they can see the result (if back hasn't just been called)
                if(self.just_called_back == False):
                    input("\n>>> Press <Return> to continue...")
                else:
                    self.just_called_back = False
        
                # Display our menu again to stop from program termination
                self.display(self._current_menu)
            else:
                self.display(self._current_menu, "Please select a valid option!")

        except KeyboardInterrupt:
            self._app.exit()

        except ValueError:
            self.display(self._current_menu, "Please select a valid option!")

