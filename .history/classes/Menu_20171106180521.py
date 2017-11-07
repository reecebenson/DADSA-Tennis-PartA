# DADSA - Assignment 1
# Reece Benson

class Menu():
    # Define the variables we will be using
    menu = {
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

    def __init__():
        #TODO: Define our Menu
        self.display()

    def display(self):
        #TODO: Display the current Menu

    def get_input(self):
        #TODO: Get user's input from defined menu

    def load_action(self, menu_id):
        #TODO: Load Action from Menu_ID