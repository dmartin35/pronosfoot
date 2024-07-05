"""
- for each fixture of the day,
- get final score from LFP
- set score in fixtures DB
- add a new entry in the table DB - for both team of the match
- calculate forecasts results - for each players for the match
"""
import datetime

from external.ligue1.api import get_score
from season.models import Fixture
from season.models import Table
from season.models import Forecast

def __calculate_points(score_home, score_away):
    #calculates the number of points for the home team given the score
    if score_home == score_away:
        return 1
    elif score_home > score_away:
        return 3
    else:
        return 0

def __team_win(score_home, score_away):
    #indicates whether home team has won
    if score_home > score_away:
        return 1
    else:
        return 0

def __team_draw(score_home, score_away):
    #indictes whether home team has drawn
    if score_home == score_away:
        return 1
    else:
        return 0

def __team_lose(score_home, score_away):
    #indicates whether home team has lost
    if score_home < score_away:
        return 1
    else:
        return 0

def __evaluate_forecast(score_a, score_b, forecast_a, forecast_b):
    """
    calculate the forecast result : points, score, issue
    
    Points attribution
    - 8 points for exact score
    ##- 5 points for winning team with correct goals difference; or draw
    - 3 points for winning team
    - 0 points otherwise
    """
    points = 0
    score = 0
    issue = 0

    if score_a == forecast_a and score_b == forecast_b:
        #8 points for good score found
        points = 8
        #match issue & score found
        score = 1
        issue = 1
    else:
        if ( (score_a == score_b and forecast_a == forecast_b) or #draw 
             (score_a > score_b and forecast_a > forecast_b) or #win
             (score_a < score_b and forecast_a < forecast_b) ): #lose
            ### 5 points for match issue found (with valid goals diff)
            # 3 points for match issue found only
            #diff = (score_a - score_b) == (forecast_a - forecast_b)
            #points = 5 if diff else 3
            points = 3
            #match issue found
            score = 0
            issue = 1
    
    return (points, score, issue)

def _check_results_date(d):
    """
    check the results for a specified date
    """
    #get the list of fixture of the day - that don't have score set
    fixtures = Fixture.objects.filter(day=d,score_a=None,score_b=None)
        
    #for each fixture of the day
    for fixture in fixtures:
        #get the score using LFP API
        (score_a, score_b) = get_score(fixture.week, 
                                       fixture.team_a.name, 
                                       fixture.team_b.name)
        
        #update the fixture object with match score
        if score_a is not None and score_b is not None:
            fixture.score_a = score_a
            fixture.score_b = score_b
            
            #and save it in the database
            fixture.save()
            
            #add a new entry in the league table - for both match teams
            Table(team=fixture.team_a,week=fixture.week,
                  points=__calculate_points(score_a,score_b),
                  win=__team_win(score_a,score_b),
                  draw=__team_draw(score_a,score_b),
                  lose=__team_lose(score_a,score_b),
                  goal_for=score_a,goal_against=score_b).save()
            Table(team=fixture.team_b,week=fixture.week,
                  points=__calculate_points(score_b,score_a),
                  win=__team_win(score_b,score_a),
                  draw=__team_draw(score_b,score_a),
                  lose=__team_lose(score_b,score_a),
                  goal_for=score_b,goal_against=score_a).save()
            
            #get the list of forecasts for the current fixture
            forecasts = Forecast.objects.filter(fixture=fixture.id)
            
            #for each forecast for the current fixture
            for forecast in forecasts:
                if forecast.score_a is not None and forecast.score_b is not None:
                    #calculate the forecast result
                    (points, score, issue) = __evaluate_forecast(fixture.score_a, 
                                                                 fixture.score_b, 
                                                                 forecast.score_a, 
                                                                 forecast.score_b)
                    
                    #update the forecast objects with points, score and issue
                    forecast.points = points
                    forecast.score = score
                    forecast.issue = issue

                    #and save it in the database
                    forecast.save()    

def check_results():
    """
    check results for fixture of the day
    """
    #get today's date
    today = datetime.date.today()
    #check results for today's date
    _check_results_date(today)


def _check_missed_results(d):
    """
    Check whether we have missed fixtures without score in the past
    """
    missed_fixtures = Fixture.objects.filter(day__lt=d, score_a=None, score_b=None)

    for mf in missed_fixtures:
        print(mf.day, mf.week, mf.team_a, mf.team_b)

    return missed_fixtures.count()


def check_missed_results():
    """
    check missed results before today (in the past)
    """
    today = datetime.date.today()
    return _check_missed_results(today)

