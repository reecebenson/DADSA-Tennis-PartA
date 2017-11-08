# DADSA - Assignment 1
# Reece Benson

from functools import partial
from os import system as call
from collections import OrderedDict

class Builder():
    _app = None
    _menu = None
    _tree = None
    _current = None

    @staticmethod
    def init(app):
        # Set our variables
        Builder._app = app
        Builder._menu = { }
        Builder._tree = [ "main" ]
        Builder._current = "main"

    @staticmethod
    def add_menu(menu, name, ref):
        # Check if this submenu exists
        if(not menu in Builder._menu):
            Builder._menu[menu] = { }

        # Update our Menu
        Builder._menu[menu].update({ ref: name })

    @staticmethod
    def add_func(name, ref, func):
        Builder._menu[ref] = func

    @staticmethod
    def get_item(ref):
        if(not ref in Builder._menu):
            return None
        else:
            return Builder._menu[ref]
        return None

    @staticmethod
    def call_func(ref):
        if(Builder.is_func(ref)):
            Builder.get_item(ref)()
        else:
            return None

    @staticmethod
    def is_func(ref):
        return callable(Builder.get_item(ref))

    @staticmethod
    def is_menu(ref):
        return not Builder.is_func(ref)

    @staticmethod
    def find_menu(index):
        # Get our current menu to check the items for
        cur_menu_items = Builder.get_item(Builder.current_menu())
        # Check that our menu exists
        if(cur_menu_items == None):
            print("There was an error with grabbing the selected menu!")
            Builder.set_current_menu("main")
            input("")
            return False
        else:
            # Iterate through our items to find our index
            for i, (k, v) in enumerate(cur_menu_items.items(), 1):
                if(index == i):
                    return { "menu": Builder.is_menu(k), "ref": k, "name": v }

            # Return Data
            return False

        # Fall back returning statement
        return False

    @staticmethod
    def show():
        print(Builder._menu)

    @staticmethod
    def current_menu():
        return Builder._current

    @staticmethod
    def set_current_menu(new_menu):
        Builder._current = new_menu
        return Builder.current_menu()

    @staticmethod
    def get_menu_tree():
        return "/".join([ m for m in Builder._tree ])

    @staticmethod
    def monitor_input():
        try:
            # Validate our input
            resp = input("\n>>> ")

            # Validate response
            if(resp.lower() == "exit" or resp.lower() == "quit"):
                # Terminate the program after user confirmation
                raise KeyboardInterrupt
            elif(resp == ""):
                # Invalid Input from User
                return Builder.show_current_menu(True, True, "You have entered an invalid option")

            # Check that the menu option exists
            try:
                # Convert our request to an integer
                req = int(resp)

                # Find the requested menu
                req_menu = Builder.find_menu(req)
                if(req_menu['menu']):
                    # Display our menu
                    Builder.set_current_menu(req_menu['ref'])
                    Builder.show_current_menu()
                else:
                    # Double check we're executing a function
                    if(Builder.is_func(req_menu['ref'])):
                        # Execute
                        Builder.call_func(req_menu['ref'])
                        input("test")
                    else:
                        print("error")
                        input("xxxxxxxxxxx")
            except Exception as err:
                input("errr!", err)
                return Builder.show_current_menu(True, True)
        except KeyboardInterrupt:
            # User has terminated the program (Ctrl+C)
            Builder._app.exit()
        except ValueError:
            # User has entered an invalid value
            Builder.show_current_menu(True, True, "You have entered an invalid option")

    @staticmethod
    def show_current_menu(shouldClear = True, error = False, errorMsg = None):
        cur_menu_items = Builder.get_item(Builder.current_menu())

        # Should we clear our terminal window?
        if(shouldClear):
            call("cls")

        # Have we got an error?
        if(error):
            if(errorMsg == None):
                print("\nError:\nThere was an error performing your request.\n")
            else:
                print(errorMsg)

        # Check that our Menu exists
        if(cur_menu_items == None):
            print("There was an error with grabbing the selected menu!")
            print("Current menu: {}".format(Builder.current_menu()))
            Builder.set_current_menu("main")
        else:
            # Print menu header
            print("Please select an option: ({0})".format(Builder.get_menu_tree()))
            
            # Print out our menu
            for i, (k, v) in enumerate(cur_menu_items.items(), 1):
                print("{0}. {1}{2}".format(i, v, (' -> ' if Builder.is_menu(k) else '')))

            # Print our back button
            if(Builder.current_menu() is not "main"):
                print("{0}. Back".format(i + 1))

            # Get input from user
            Builder.monitor_input()

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
        # Create our Menu
        Builder.init(self._app)

        ## MAIN
        Builder.add_menu("main", "Load Season", "load_season")
        Builder.add_menu("main", "See Developer Information", "info")
        Builder.add_func("main", "info", lambda: self.dev_info())

        ## LOAD SEASON
        for season_id in self._app.handler.get_seasons():
            season = self._app.handler.get_season(season_id)
            Builder.add_menu("load_season", season.name(), "ls_[{0}]".format(season.name()))

        ## SHOW MENU
        Builder.show_current_menu()

        ## HALT
        """input("HALT!")

        # Clear our menu variables
        self._menu = { }
        self._current = [ "main" ]
        self._current_menu = "main"
        self.just_called_back = False

        # Create our Menu
        self._menu['main'] = { "load_season": "Load Season", "info": "See Developer Information" }
        self._menu['info'] = lambda: self.dev_info()
        self._menu['back'] = lambda: self.go_back()
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

                # Define menu holders
                self._menu[tournamentVar] = { }
                self._menu[tournamentVar+"_rselect"] = { }

                # Tournament Selecter
                self._menu[seasonVar+"_select"].update({ tournamentVar: "Select {0}".format(tournament_name) })

                # > "View Rounds"
                self._menu[tournamentVar].update({ tournamentVar+"_rselect": "View Rounds" })

                # > Populate "View Rounds" with Round specific otpions
                for gdr in season.rounds():
                    # List genderd rounds
                    self._menu[tournamentVar+"_rselect"].update({ tournamentVar+"_"+gdr: "{0} rounds".format(gdr).title() })

                    # List the available rounds within the menu
                    self._menu[tournamentVar+"_"+gdr] = { }
                    for r, rnd in enumerate(season.rounds()[gdr], 1):
                        self._menu[tournamentVar+"_"+gdr].update({ tournamentVar+"-"+gdr+"-"+rnd: "Round {0}".format(r) })
                        self._menu[tournamentVar+"-"+gdr+"-"+rnd] = partial(print, "\n".join([ "{0} — Winner: {1}, updated score: {2}".format(m.versuses(True), m.winner()[0].name(), season.round(gdr, rnd).get_rank()) for m in season.round(gdr, rnd).matches() ]))

                    # Add the back option
                    self._menu[tournamentVar+"_"+gdr].update({ "back": "Back" })

                # Add tournament specific options
                self._menu[tournamentVar].update({ tournamentVar+"_leaderboard": "View Leaderboard", tournamentVar+"_difficulty": "View Difficulty", tournamentVar+"_prizemoney": "View Prize Money" })
                self._menu[tournamentVar+"_leaderboard"] = partial(print, season.tournament(tournament_name).display("leaderboard"))
                self._menu[tournamentVar+"_difficulty"] = partial(print, season.tournament(tournament_name).display("difficulty"))
                self._menu[tournamentVar+"_prizemoney"] = partial(print, season.tournament(tournament_name).display("prize_money"))

                # Add the back option
                self._menu[tournamentVar].update({ "back": "Back" })
                self._menu[tournamentVar+"_rselect"].update({ "back": "Back" })

            # > "View Players"
            for gdr in season.players():
                self._menu[seasonVar+"_players"].update({ seasonVar+"_players_"+gdr: "List {0}s".format(gdr.title()) })
                self._menu[seasonVar+"_players_"+gdr] = partial(print, season.display("players", gdr))

            # Add the back options to each submenu
            self._menu[seasonVar+"_select"].update({ "back": "Back" })
            self._menu[seasonVar+"_players"].update({ "back": "Back" })
        self._menu["load_season"].update({ "back": "Back" })

        # Display our Menu
        self.display("main")"""

    def dev_info(self):
        # Display Developer Information
        print("Python - Design and Analysis of Data Structures and Algorithms")
        print("Assignment 1, due 30th of November 2017")
        print("")
        print("This implementation was developed by Reece Benson")
        print("Student ID: 16021424")
        print("Student Email: Reece2.Benson@live.uwe.ac.uk")
        print("")
        print("The GitHub repository can be found @ http://github.com/reecebenson/DADSA-Tennis (private repo)")
        print("Thanks!")

        # Go back to the menu
        input("\n>>> Press <Return> to continue...")
        self.display(self._current_menu)

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
                    input(">>> Press <Return> to continue...")
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

