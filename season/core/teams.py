"""
TEAMS MANAGEMENT
"""
from season.models import Team

__all__ = ['isTeamValid','firstAvailableTeam','getAllTeams','getTeamName']

def isTeamValid(team_id):
    """
    check whether team id is valid in the DB
    """
    try:
        Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return False
    else:
        return True

def firstAvailableTeam():
    """
    returns the id of the first team from the DB
    """
    return Team.objects.order_by('name').all()[0]

def getAllTeams():
    """
    returns the entire list of teams 
    """
    return Team.objects.order_by('name').all()

def getTeamName(team_id):
    """
    returns the team name corresponding to the given id
    """
    try:
        return Team.objects.get(id=team_id).name
    except Team.DoesNotExist:
        return None
