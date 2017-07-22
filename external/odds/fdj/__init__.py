import os

FDJ_TEAM_MAP = {}


def init_team_map():
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, 'teams.txt')
    with open(path) as fhnd:
        for line in fhnd:
            fdj_name, custom_name = line.strip().split(':')
            FDJ_TEAM_MAP[fdj_name] = custom_name


#initializes the global dict for team names
init_team_map()
