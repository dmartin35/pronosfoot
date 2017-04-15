"""
TABLES MANAGEMENT
"""
from season.queries import league_table
from season.queries import league_table_with_teamid
from season.queries import league_table_until
from season.queries import user_table_with_bonus
from season.queries import user_table_until_week
from season.queries import user_table_for_week
from season.queries import league_table_until_with_teamid
from season.models import Table
from tools.utils import distinct
from tools.utils import list_evolution
from tools.utils import list_to_dict

__all__ = ['full_league_table','full_league_table_until',
           'last_played_week','full_league_table_auto',
           'played_weeks','full_players_table_with_bonus',
           'full_players_table_until','full_players_table_until_auto',
           'full_league_table_teamid','team_played_weeks',
           'full_league_table_until__dict']

#LEAGUE TABLE

def full_league_table():
    """
    returns the full league table
    """
    return [list(x) for x in league_table()]

def full_league_table_teamid():
    """
    returns the full league table, with team id
    """
    return [list(x) for x in league_table_with_teamid()]

def full_league_table_until(week):
    """
    returns the league table until a given week (included) 
    """
    table = [list(x) for x in league_table_until(week)]
    if week > 1:
        table_last = [list(x) for x in league_table_until(week-1)]
        #calculate team position evolution (by team name)
        evo = list_evolution([x[0] for x in table], [x[0] for x in table_last])
        #extend table with position evolution (last item)
        for idx in range(0,len(table)):
            table[idx].extend([evo[idx]])
    return table

TEAMS_TABLE_KEYS = ['id','name','pts','played','win','draw','lose','goal_for','goal_against','diff']
TEAMS_TABLE_EVO_KEYS = ['id','name','pts','played','win','draw','lose','goal_for','goal_against','diff','evo']

def full_league_table_until__dict(week):
    """
    returns the league table until a given week (included)
    (each line is a dict) 
    """
    table = [list(x) for x in league_table_until_with_teamid(week)]
    if week > 1:
        table_last = [list(x) for x in league_table_until_with_teamid(week-1)]
        #calculate team position evolution (by team name)
        evo = list_evolution([x[0] for x in table], [x[0] for x in table_last])
        #extend table with position evolution (last item)
        for idx in range(0,len(table)):
            table[idx].extend([evo[idx]])
        #convert list of list to list of dict
        return [list_to_dict(TEAMS_TABLE_EVO_KEYS, x) for x in table]
    #convert list of list to list of dict
    return [list_to_dict(TEAMS_TABLE_KEYS, x) for x in table]

def played_weeks():
    """
    returns the list of played weeks
    for which there is an entry in the league table
    """
    return distinct([t.week for t in Table.objects.filter(week__gt=0).order_by('week').all()])

def team_played_weeks(team_id):
    """
    returns the list of played weeks for a team 
    for which there is an entry in the league table
    """
    return [t.week for t in Table.objects.filter(team=team_id,week__gt=0).order_by('week').all()]

def last_played_week():
    """
    returns the last number of played weeks
    for which there is an entry in the league table
    """
    played = distinct([t.week for t in Table.objects.filter(week__gt=0).order_by('week').all()])
    return played[-1:][0] if played != [] else 0

def full_league_table_auto():
    """
    returns the league table until last available week (included)
    """
    week = last_played_week()
    return full_league_table_until(week)

#PLAYERS TABLE
PLAYERS_TABLE_KEYS = ['id','name','pts','scores','issues','matches']
PLAYERS_TABLE_EVO_KEYS = ['id','name','pts','scores','issues','matches','evo']
PLAYERS_TABLE_BONUS_KEYS = ['id','name','pts','scores','issues','matches','total','bonus']
PLAYERS_TABLE_BONUS_EVO_KEYS = ['id','name','pts','scores','issues','matches','total','bonus','evo']

def full_players_table_with_bonus():
    """
    returns the full table for players  
    with bonus handled for total points
    
    evolution is checked again the full 
    table for players - a week before the last -
    """
    user_table_bonus = [list(x) for x in user_table_with_bonus()]
    user_table = [list(x) for x in user_table_until_week(last_played_week()-1)]
    #calculate player position evolution (by player name)
    evo = list_evolution([x[0] for x in user_table_bonus], [x[0] for x in user_table])
    #extend table with position evolution (last item)
    for idx in range(0,len(user_table_bonus)):
        user_table_bonus[idx].extend([evo[idx]])
    #convert list of list to list of dict
    return [list_to_dict(PLAYERS_TABLE_BONUS_EVO_KEYS, x) for x in user_table_bonus]

def full_players_table_until(week):
    """
    returns the players table until a given week 
    """
    user_table = [list(x) for x in user_table_until_week(week)]
    if week > 1:
        user_table_last = [list(x) for x in user_table_until_week(week-1)]
        #calculate player position evolution (by player name)
        evo = list_evolution([x[0] for x in user_table], [x[0] for x in user_table_last])
        #extend table with position evolution (last item)
        for idx in range(0,len(user_table)):
            user_table[idx].extend([evo[idx]])
        return [list_to_dict(PLAYERS_TABLE_EVO_KEYS, x) for x in user_table]
    return [list_to_dict(PLAYERS_TABLE_KEYS, x) for x in user_table]
    
def full_players_table_until_auto():
    """
    returns the players table until last available week (included)
    """
    week = last_played_week()
    return full_players_table_until(week)

def full_players_table_for_week(week):
    """
    returns the player table of the week, for a given week
    """
    return [list_to_dict(PLAYERS_TABLE_KEYS, list(x)) for x in user_table_for_week(week)]