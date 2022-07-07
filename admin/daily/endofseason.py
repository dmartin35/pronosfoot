"""
- check end of season
- calculate bonus points for season forecasts
"""
from season.models import LeagueForecast
from season.core.season import endOfSeason
from season.core.season import midSeasonWeek
from season.core.tables import full_league_table_until
from season.core.tables import full_league_table_teamid

def check_season_results():
    """
    check results for season forecasts
    at the end of the season
    """
    if endOfSeason():
        #get the list of forecasts for the season
        season_forecasts = LeagueForecast.objects.all()
        
        #get the results for the season
        season_results = _get_season_results()
        
        #for each forecast, 
        for season_forecast in season_forecasts:
            #if points have not been calculated before
            if not season_forecast.points:
                #calculate the number of points
                points = 0
                bonus = 20
                
                try:
                    for attribute in ['winner_midseason','winner','second','third','fourth','fifth']:
                        value = str(getattr(season_forecast, attribute))
                        if value == season_results[attribute]:
                            points += bonus
                    for attribute in ['looser1','looser2','looser3','looser4']:
                        value = str(getattr(season_forecast, attribute))
                        if value in season_results['lasts']:
                            points += bonus
                except:
                    pass
                
                #update season forecast with calculated points
                season_forecast.points = points
                
                #and save it in the databse
                season_forecast.save()
                
def _get_season_results():
    """
    returns a dict containing results of the season: 
    winner, second, etc.
    """
    season_results = {}
    season_results['winner_midseason'] = None
    season_results['winner'] = None
    season_results['second'] = None
    season_results['third'] = None
    season_results['fourth'] = None
    season_results['fifth'] = None
    season_results['lasts'] = None
    
    #get the mid-season league table
    try:
        league_table_midseason = full_league_table_until(midSeasonWeek())
        season_results['winner_midseason'] = str(league_table_midseason[0][0])
    except: 
        pass
    
    #get the final league table
    try:
        league_table = full_league_table_teamid()
        for (key,idx) in [('winner',0),('second',1),('third',2),('fourth',3),('fifth',4)]:
            season_results[key] = str(league_table[idx][1])
        season_results['lasts'] = [str(x[1]) for x in league_table[-4:]]
    except:
        pass
    
    return season_results
    