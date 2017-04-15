"""
SEASON GLOBAL
"""
from season.models import Fixture
from season.core.weeks import getAllWeeks

__all__ = ['endOfSeason','midSeasonWeek','midSeason']

def endOfSeason():
    """
    indicates whether the season is finished
    i.e. all fixtures have a final score 
    """
    return Fixture.objects.filter(score_a=None,score_b=None).count() == 0

def midSeasonWeek():
    """
    returns the number of the week of the mid season
    """
    try:
        #mid season week
        return int(int(getAllWeeks()[-1])/2)
    except: 
        pass
    #should not get here
    return 0

def midSeason():
    """
    indicates whether the season has reached end of first half
    i.e. all first half fixtures have a final score
    """
    return Fixture.objects.filter(week__lte=midSeasonWeek(),score_a=None,score_b=None).count() == 0
    