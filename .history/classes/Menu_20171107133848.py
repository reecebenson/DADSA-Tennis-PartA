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
        self._menu = {
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
        cur_count = 0
        m = self.get_current_menu()
        for i in m:
            # Is the Menu Item a Function?
            m_type = None
            if(callable(m[i])): m_type = ""
            else:               m_type = "->"
            
            cur_count += 1
            print("{0}. {1}".format(cur_count, i, m_type))

        # Get User Input
        self.get_input()

    def get_current_menu(self):
        index = self._current_menu
        return self._menu[index]

    def get_menu(self, menu):
        m = self._menu.items()
        print(m[menu])

    def get_input(self):
        resp = input(">>> ")
        self.get_menu(resp)

    def load_action(self, menu_id):
        #TODO: Load Action from Menu_ID
        print("Load Action")