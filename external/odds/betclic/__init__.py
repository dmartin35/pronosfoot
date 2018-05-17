import os

TEAM_MAP = {}


def init_team_map():
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, 'teams.txt')
    with open(path) as fhnd:
        for line in fhnd:
            name, custom_name = line.strip().split(':')
            TEAM_MAP[name] = custom_name


#initializes the global dict for team names
init_team_map()
