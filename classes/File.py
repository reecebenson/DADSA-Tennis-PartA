import json

class File():
    @staticmethod
    def update_season_rounds(season, new_rounds):
        with open('data/seasons.json', 'r+') as f:
            data = json.load(f)

            # Check our Season exists
            if(season in data):
                # Append our new_rounds to the current data
                data[season]['rounds'] = new_rounds

                # Seek back to SOF and write back our data
                f.seek(0)
                f.write(json.dumps(data, indent=4))
                f.truncate()
            else:
                return False
        return True
    
    def add_gender(season, gender, cap):
        with open('data/players.json', 'r+') as f:
            data = json.load(f)

            # Check our Season exists
            if(season in data):
                # Add our gender to the season
                data[season].update({ gender: [ ] })

                # Update
                f.seek(0)
                f.write(json.dumps(data, indent=4))
                f.truncate()

                return True
            else:
                return False
        return False

    def add_player(season, gender, name):
        with open('data/players.json', 'r+') as f:
            data = json.load(f)

            # Check our Season exists
            if(season in data):
                # Check our Gender exists
                if(gender in data[season]):
                    # Append our player to the list
                    data[season][gender].append(name)

                    # Update
                    f.seek(0)
                    f.write(json.dumps(data, indent=4))
                    f.truncate()
                    return True
                else:
                    return False
            else:
                return False
        return False

    def update_settings(season, name, value):
        with open('data/seasons.json', 'r+') as f:
            data = json.load(f)

            # Check our Season exists
            if(season in data):
                # Check if our setting exists
                if(name in data['settings']):
                    # Update setting
                    data['settings'][name] = value
                else:
                    # Create setting
                    data['settings'].update({ name: value })

                # Update
                f.seek(0)
                f.write(json.dumps(data, indent=4))
                f.truncate()
            else:
                return False
        return True
