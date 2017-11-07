# DADSA - Assignment 1
# Reece Benson
import json

class Handler():
    def __init__(self):
        print("HANDLIN FUCK ALL")

    def load_players(self):
        with open('./data/players.json') as tData:
            data = json.load(tData)

            print(data)