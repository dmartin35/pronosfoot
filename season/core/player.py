"""
PLAYERS MANAGEMENT
"""
from season.models import Player

__all__ = ['isPlayerValid','getAllPlayers','getPlayerName']

def isPlayerValid(player_id):
    """
    check whether player id is valid in the DB
    """
    try:
        Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return False
    else:
        return True
    
def getAllPlayers():
    """
    returns the entire list of players 
    """
    return Player.objects.order_by('name').all()
    
def getPlayerName(player_id):
    """
    returns the player name corresponding to the given id
    """
    try:
        return Player.objects.get(id=player_id).name
    except Player.DoesNotExist:
        return None