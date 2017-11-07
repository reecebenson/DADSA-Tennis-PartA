# DADSA - Assignment 1
# Reece Benson

class Menu():
    # Define the variables we will be using
    _app = None
    _menu = None
    _current_menu = [ 0 ]

    def __init__(self, app):
        # Set our Application
        self._app = app

    def load(self):
        # Define our Menu
        self.menu = {
            'Item 1': {
                'Sub Item 1': self.load_action,
                'Sub Item 2': self.load_action
            },
            
            'Item 2': {
                'Sub Item 1': self.load_action,
                'Sub Item 2': self.load_action,
                'Sub Item 3': self.load_action,
                'Sub Item 4': self.load_action
            },

            'Item 3': self.load_action,

            'Item 4': {
                'Sub Item 1': {
                    'Sub Sub Item 1': self.load_action,
                    'Sub Sub Item 2': self.load_action
                }
            }
        }

        # Display our Menu
        self.display()

    def display(self):
        #TODO: Display the current Menu
        self.get_current_menu()

    def get_current_menu(self):
        # Retrieve our current index [x, y, z]
        index = self._current_menu

        # ITS FUCKEEEEEEEEEEEEEED
        print(self.menu[index])

    def get_input(self):
        #TODO: Get user's input from defined menu
        print("Get Input")

    def load_action(self, menu_id):
        #TODO: Load Action from Menu_ID
        print("Load Action")