# DADSA - Assignment 1
# Reece Benson

class Menu():
    # Define the variables we will be using
    _app = None
    _menu = None
    _current_menu = "main"

    def __init__(self, app):
        # Set our Application
        self._app = app

    def load(self):
        # Define our Menu
        self.menu = {
            # Main Menu
            'main':
            {
                'New Season': 'new_season',
                'Load Season': 'load_season'
            },
            
            # New Season
            'new_season':
            {
                'Sub Item 1': self.load_action,
                'Sub Item 2': self.load_action,
                'Sub Item 3': self.load_action,
                'Sub Item 4': self.load_action
            },

            # Load Season
            'load_season':
            {
                'Sub Item 1': {
                    'Sub Sub Item 1': self.load_action,
                    'Sub Sub Item 2': self.load_action
                }
            }
        }

        # Display our Menu
        self.display()

    def display(self):
        m = self.get_current_menu()
        for i in range(len(m)):
            # Get our Menu Item
            _m = m[i]

            # Display Menu Item
            print("{0}. {1} {2}".format(i, m, i))

    def get_current_menu(self):
        index = self._current_menu
        return self.menu[index]

    def get_input(self):
        #TODO: Get user's input from defined menu
        print("Get Input")

    def load_action(self, menu_id):
        #TODO: Load Action from Menu_ID
        print("Load Action")