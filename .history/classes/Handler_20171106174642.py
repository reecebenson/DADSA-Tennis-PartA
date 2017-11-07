# DADSA - Assignment 1
# Reece Benson
import json

class Handler():
    def __init__(self):
        print("HANDLIN FUCK ALL")

    def load_players(self):
        players = []

        with open('./data/players.json') as tData:
            data = json.load(tData)

            for gender in data:
                if(not gender in players):
                    players[gender] = []

                for player in data[gender]:
                    players[gender].append(player)
                    print(player)