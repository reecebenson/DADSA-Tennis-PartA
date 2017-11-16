# DADSA - Assignment 1
# Reece Benson

from os import system as call

class Round():
    _app = None
    _name = None
    _gender = None
    _parent = None
    _previous_round = None
    _players = None
    _matches = None
    _match_count = None
    _cap = 3

    def __init__(self, app=None, gender=None, name=None, parent=None, match_cap=None):
        # Set our application
        self._app = app

        # Set our variables
        self._name = name
        self._parent = parent
        self._gender = gender
        self._previous_round = None
        self._players = [ ]
        self._matches = [ ]
        self._match_cap = match_cap

    def name(self):
        return self._name

    def parent(self):
        return self._parent

    def players(self):
        return self._players

    def previous_round(self):
        return self._previous_round

    def set_previous_round(self, prev):
        self._previous_round = prev
        return self.previous_round()

    def validate(self, error_count = 0):
        # Check if this round is statistically correct
        error = False
        
        # Check if the rounds are above the cap
        if(len(self.matches()) > self.match_cap()):
            # Error Occurred
            error = True
            error_count += 1

            # Print out the match for the user to see and reference to
            call("cls")
            print("Match Cap: {}, current match count: {}".format(self.match_cap(), len(self.matches())))

            print("CHECK MATCHES, NON-WINNERS IN PREV ROUND ETC.")
            new_score = input(">>> ")
            if(new_score.isdigit()):
                new_score = int(new_score)
                if(new_score >= 0 and new_score <= cap):
                    self._player_one_score = new_score
                else:
                    return self.validate(error_count)
            else:
                return self.validate(error_count)

        # Clear our variables
        self._players.clear()
        matchId = 0
        
        # Check that a player hasn't played twice
        for m in self.matches():
            # Increase Match Identifier
            matchId += 1

            if(m.player_one()[0] == None or m.player_two()[0] == None):
                call("cls")
                print("There was an error with processing round data. The data is corrupt and has players that do not exist.\nPlease regenerate the 'seasons.json' file.")
                return self._app.exit()

            # Check Player One
            if(m.player_one()[0].name() in self.players()):
                error = True
                error_count += 1

                # Print some details
                call("cls")
                print("[{0}:{1}] {2} is already in the player list for Match {3}. Fixing...".format(self.parent().name(), self.name(), m.player_one()[0].name(), matchId))

                # Get user not in this list
                if(self.previous_round() != None):
                    # Find a player that doesn't exist within this round but exists within the previous round
                    p_found = [ False, None ]
                    for p in self.previous_round().players():
                        if(p not in self.players() and (p in [ w.name() for w in self.previous_round().winners() ])):
                            p_found = [ True, m.player_one()[0].name() ]
                            m._player_one = self.parent().season().player(m.player_one()[0].gender(), p)
                            break

                    # Check if the error has been resolved
                    if(p_found[0]):
                        # Update 'seasons.json'
                        input("[{2}:{3}] '{0}' has been replaced with '{1}' - ...continue\n".format(p_found[1], p, self.parent().name(), self.name()))
                    else:
                        call("cls")
                        print("There was an error with processing round data. The data is corrupt and has players that do not exist.\nPlease regenerate the 'seasons.json' file.")
                        return self._app.exit()
                else:
                    # Find a player that doesn't exist within this round but exists within the previous round
                    p_found = [ False, None ]
                    for p in self.parent().season().players():
                        if(p not in self.players() and (p in [ w.name() for w in self.parent().season().players()[m.player_one()[0].gender()] ])):
                            p_found = [ True, m.player_one()[0].name() ]
                            m._player_one = self.parent().season().player(m.player_one()[0].gender(), p)
                            break

                    # Check if the error has been resolved
                    if(p_found[0]):
                        # Update 'seasons.json'
                        input("[{2}:{3}] '{0}' has been replaced with '{1}' - ...continue\n".format(p_found[1], p, self.parent().name(), self.name()))
                    else:
                        call("cls")
                        print("There was an error with processing round data. The data is corrupt and has players that do not exist.\nPlease regenerate the 'seasons.json' file.")
                        return self._app.exit()
            else:
                self._players.append(m.player_one()[0].name())
            
            # Check Player Two
            if(m.player_two()[0].name() in self.players()):
                error = True
                error_count += 1

                # Print some details
                call("cls")
                print("[{0}:{1}] {2} is already in the player list for Match {3}. Fixing...".format(self.parent().name(), self.name(), m.player_two()[0].name(), matchId))

                # Get user not in this list
                if(self.previous_round() != None):
                    # Find a player that doesn't exist within this round but exists within the previous round
                    p_found = [ False, None ]
                    for p in self.previous_round().players():
                        if(p not in self.players() and (p in [ w.name() for w in self.previous_round().winners() ])):
                            p_found = [ True, m.player_two()[0].name() ]
                            m._player_two = self.parent().season().player(m.player_two()[0].gender(), p)
                            break

                    # Check if the error has been resolved
                    if(p_found[0]):
                        # Update 'seasons.json'
                        input("[{2}:{3}] '{0}' has been replaced with '{1}' - ...continue\n".format(p_found[1], p, self.parent().name(), self.name()))
                    else:
                        call("cls")
                        print("There was an error with processing round data. The data is corrupt and has players that do not exist.\nPlease regenerate the 'seasons.json' file.")
                        return self._app.exit()
                else:
                    # Find a player that doesn't exist within this round but exists within the previous round
                    p_found = [ False, None ]
                    for p in self.parent().season().players():
                        if(p not in self.players() and (p in [ w.name() for w in self.parent().season().players()[m.player_two()[0].gender()] ])):
                            p_found = [ True, m.player_two()[0].name() ]
                            m._player_two = self.parent().season().player(m.player_two()[0].gender(), p)
                            break

                    # Check if the error has been resolved
                    if(p_found[0]):
                        # Update 'seasons.json'
                        input("[{2}:{3}] '{0}' has been replaced with '{1}' - ...continue\n".format(p_found[1], p, self.parent().name(), self.name()))
                    else:
                        call("cls")
                        print("There was an error with processing round data. The data is corrupt and has players that do not exist.\nPlease regenerate the 'seasons.json' file.")
                        return self._app.exit()
            else:
                self._players.append(m.player_two()[0].name())

            # Check that the players are within the winners of the previous round (if exists)
            if(self.previous_round() != None):
                existing_players = [ p for p in self.players() ]
                winner_name_list = [ w.name() for w in self.previous_round().winners() ]
                
                # Check Player One exists within the previous winners
                if(m.player_one()[0].name() not in winner_name_list):
                    # Print some details
                    call("cls")
                    print(winner_name_list)
                    print("[{0}:{1}] Player {2} was not a valid winner for the previous {3}. Fixing...".format(self.parent().name(), self.name(), m.player_one()[0].name(), self.previous_round().name()))

                    # Find a player who is not defined within these matches
                    p_found = [ False, None ]
                    for p in self.previous_round().winners():
                        if(p.name() in winner_name_list and p.name() not in existing_players):
                            p_found = [ True, p.name() ]
                            if(self.parent().season().player(m.player_one()[0].gender(), p.name()) == None):
                                input("fucked it")
                            print(self.parent().season().player(m.player_one()[0].gender(), p.name()))
                            m._player_one = self.parent().season().player(m.player_one()[0].gender(), p.name())

                    # If we have a player, lets fix our data
                    if(p_found[0]):
                        # Update 'seasons.json'
                        input("[{2}:{3}] '{0}' has been replaced with '{1}' - ...continue\n".format(m.player_one()[0].name(), p_found[1], self.parent().name(), self.name()))
                    else:
                        input("Unable to fix this shit...")
                        exit()

                # Check Player Two exists within the previous winners
                if(m.player_two()[0].name() not in winner_name_list):
                    # Print some details
                    call("cls")
                    print(winner_name_list)
                    print("[{0}:{1}] Player {2} was not a valid winner for the previous {3}. Fixing...".format(self.parent().name(), self.name(), m.player_two()[0].name(), self.previous_round().name()))

                    # Find a player who is not defined within these matches
                    p_found = [ False, None ]
                    for p in self.previous_round().winners():
                        if(p.name() in winner_name_list and p.name() not in existing_players):
                            p_found = [ True, p.name() ]
                            m._player_two = self.parent().season().player(m.player_two()[0].gender(), p.name())

                    # If we have a player, lets fix our data
                    if(p_found[0]):
                        # Update 'seasons.json'
                        input("[{2}:{3}] '{0}' has been replaced with '{1}' - ...continue\n".format(m.player_two()[0].name(), p_found[1], self.parent().name(), self.name()))
                    else:
                        input("Unable to fix this shit...")
                        exit()

        # Check if we're done (aggressive recursion)
        if(error):
            return self.validate(error_count)
        else:
            return error_count

    def gender(self):
        return self._gender

    def match_cap(self):
        return self._match_cap

    def set_match_cap(self, cap):
        self._match_cap = cap
        return self.match_cap()

    def cap(self):
        return self._cap

    def set_cap(self, cap):
        self._cap = cap
        return self.cap()

    def add_match(self, match):
        self._matches.append(match)

    def matches(self):
        return self._matches

    def match_count(self):
        return len(self.matches())

    def get_rank(self):
        return "n/a"

    def winners(self):
        _winners = [ w.winner()[0] for w in self.matches() ]
        return _winners