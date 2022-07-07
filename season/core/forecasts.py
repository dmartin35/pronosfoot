"""
FORECASTS AND RESULTS
"""
import datetime
from django.forms.models import formset_factory
from season.models import Player
from season.models import Fixture
from season.models import Forecast
from season.forms import ForecastForm
from season.models import LeagueForecast
from season.forms import LeagueForecastForm
from season.core.fixtures import fixtures as fixturesList
from season.core.fixtures import countFixuresPerDayForMonth
from season.core.fixtures import fixturesOfTheDay
from django.conf import settings
from season.queries import user_total
from season.core.season import midSeason
from season.core.season import midSeasonWeek
from season.core.season import endOfSeason
from season.core.tables import full_league_table
from season.core.tables import full_league_table_until
from season.core.fixtures import hasFixtureStarted

__all__ = ['forecasts','hasForecastsForWeek',
           'getForecastsFormset','saveForecastsFormset',
           'getLeagueForecastsForm','saveLeagueForecastsForm',
           'countForecastsForMonth','mergeForecastFormsetAdditionalInfo',
           'forecastsTotalPointsForWeek','forecastResult',
           'leagueForecastsResults','leagueForecastsResultsForPlayer',
           'getFixtureForecasts'
           ]

def forecasts(week,player):
    """
    returns the forecasts for a specified week and player;
    with forecast results if available 
    """
    pass

def hasForecastsForWeek(week):
    """
    indicates whether forecasts exist for the required week
    """
    return Forecast.objects.filter(fixture__week=week).count() != 0

def getForecastsFormset(week,player):
    """
    returns the form set of forecasts for a player and a specific week
    """
    #list of fixtures of the week
    fixtures = fixturesList(week)

    player = Player.objects.get(id=player)
    
    #create the list of fixtures ids to be passed as initial data to forms
    initialdata = []
    week_points = []
    for fixture in fixtures:
        data = {'fixture': fixture.id, 'user_id': player.id}
        pts = None
        
        #try to get existing forecast scores
        forecast = Forecast.objects.filter(user=player, fixture=fixture)
        if forecast:
            data.update(forecast.values('score_a', 'score_b')[0])
            pts = forecast.values('points')[0]['points']
        initialdata.append(data)
        week_points.append(pts)
    
    #create the formset
    ForecastFormSet = formset_factory(form=ForecastForm, max_num=len(fixtures))
    formset = ForecastFormSet(initial=initialdata)
    
    currenttime = datetime.datetime.now()
    for idx in range(len(fixtures)):
        #add fixtures additional information for forecast forms
        formset.forms[idx].fixture_id = fixtures[idx].id
        formset.forms[idx].team_a = fixtures[idx].team_a
        formset.forms[idx].team_b = fixtures[idx].team_b
        formset.forms[idx].day = fixtures[idx].day
        formset.forms[idx].hour = fixtures[idx].hour
        #indicates whether forecast can still be set - before match start time
        fixturetime = datetime.datetime(fixtures[idx].day.year,
                                        fixtures[idx].day.month,
                                        fixtures[idx].day.day,
                                        fixtures[idx].hour.hour,
                                        fixtures[idx].hour.minute,
                                        fixtures[idx].hour.second,
                                        fixtures[idx].hour.microsecond)
        formset.forms[idx].readonly = currenttime >= fixturetime
        #add forecasts results points to forecast forms
        formset.forms[idx].points = week_points[idx]
        #add number of forecasts - for all players - for current fixture
        formset.forms[idx].nb_forecasts = len(Forecast.objects.filter(fixture__id=fixtures[idx].id).all())
        
    return formset

def mergeForecastFormsetAdditionalInfo(formset1,formset2):
    """
    merge forecasts formset additional info from formset1 to formset2
    returns merged formset2
    """
    for idx in range(0,len(formset1.forms)):
        formset2.forms[idx].fixture_id = formset1.forms[idx].fixture_id
        formset2.forms[idx].team_a = formset1.forms[idx].team_a
        formset2.forms[idx].team_b = formset1.forms[idx].team_b
        formset2.forms[idx].day = formset1.forms[idx].day
        formset2.forms[idx].hour = formset1.forms[idx].hour
        formset2.forms[idx].readonly = formset1.forms[idx].readonly
        formset2.forms[idx].points = formset1.forms[idx].points
        formset2.forms[idx].nb_forecasts = formset1.forms[idx].nb_forecasts
    return formset2
    
def saveForecastsFormset(request):
    """
    validate and save a forecasts formset from the given request
    
    returns a boolean indicating whether the form set has been saved or not;
    plus the formset in case of errors - None if no errors 
    """
    saved = False
    formset = None
    
    if request.method == 'POST':
        ForecastFormSet = formset_factory(form=ForecastForm)
        formset = ForecastFormSet(request.POST)
        if formset.is_valid():
            for form in formset.forms:
                form.save()
            saved = True
    
    return (saved,formset)

def getLeagueForecastsForm(player):
    """
    return the form of league forecasts for a player
    """
    player = Player.objects.get(id=player)
    try:
        #get the league forecast for a player
        forecasts = LeagueForecast.objects.get(user=player)
    except LeagueForecast.DoesNotExist:
        #creates a new entry for the user
        forecasts = LeagueForecast(user=player)
        forecasts.save(force_insert=True)

    initialdata = {'user_id':player.id,
                   'winner_midseason':forecasts.winner_midseason.id if forecasts.winner_midseason else None, 
                   'winner':forecasts.winner.id if forecasts.winner else None,
                   'second':forecasts.second.id if forecasts.second else None,
                   'third':forecasts.third.id if forecasts.third else None,
                   'fourth':forecasts.fourth.id if forecasts.fourth else None,
                   'fifth': forecasts.fifth.id if forecasts.fifth else None,
                   'looser1':forecasts.looser1.id if forecasts.looser1 else None,
                   'looser2':forecasts.looser2.id if forecasts.looser2 else None,
                   'looser3':forecasts.looser3.id if forecasts.looser3 else None,
                   'looser4': forecasts.looser4.id if forecasts.looser4 else None,
                   }

    #create form with forecasts data    
    form = LeagueForecastForm(initial=initialdata)

    #add additional information for forecast form
    currenttime = datetime.datetime.now()
    
    #disable edition mode, if vote limit date has expired
    form.readonly = currenttime > settings.SEASON_FORECAST_MAX_DATE
    
    return form

def saveLeagueForecastsForm(request):
    """
    validate and save league forecasts from the given request
    
    returns a boolean indicating whether the form has been saved or not
    plus the form in case of errors - None if no errors
    """
    saved = False
    form = None
    
    if request.method == 'POST':
        form = LeagueForecastForm(request.POST)
        if form.is_valid():
            form.save()
            saved = True
    
    #in case of error form,
    if not saved and form: 
        #add additional information for forecast form
        currenttime = datetime.datetime.now()
        #disable edition mode, if vote limit date has expired
        form.readonly = currenttime > settings.SEASON_FORECAST_MAX_DATE
    
    return (saved,form)
    
def countForecastsForMonth(year,month,player):
    """
    returns a dict indicating whether a player has saved 
    all its forecasts for all matches for all match of the month
    key is the day number, value is the indicator (empty,half,full) 
    """
    forecasts_count = {}
    fixturescount = countFixuresPerDayForMonth(year,month)
    for line in fixturescount:
        count = line['count']
        day = line['day']

        day_fixtures_ids = list([int(f.id) for f in fixturesOfTheDay(day)])
        
        #get the forecasts of the current player for the day
        where = 'fixture_id IN %s AND user_id = %d AND score_a is not NULL and score_b is not NULL' % (tuple(day_fixtures_ids).__str__(),player)
        where = where.replace(",)", ")") #remove tailing comma in case of one element list
        forecasts_day = Forecast.objects.extra(where=[where])
        num_forecasts_day = len(forecasts_day)       
 
        #save the information about current day (% of forecast done)
        if num_forecasts_day == count:
            forecasts_count[day.day] = 'full'
        elif num_forecasts_day <count and num_forecasts_day > 0:
            forecasts_count[day.day] = 'half'
        elif num_forecasts_day == 0:
            forecasts_count[day.day] = 'empty'
        else:
            forecasts_count[day.day] = ''

    return forecasts_count

def forecastsTotalPointsForWeek(week,player):
    """
    returns the number total of points for the player
    for the week forecasts
    returns the number if available; None otherwise
    """
    #gets the user's total points for the selected week
    total = user_total(week=week, user=player)
    try:
        total = int(total[0][0])
    except: 
        total = None
    return total

def forecastResult(fixture_id,player):
    """
    return the fixture forecast result of the player 
    """
    results = None
    forecast = Forecast.objects.filter(user__id=player, fixture__id=fixture_id)
    if forecast:
        results = forecast.values('points', 'score', 'issue')[0]
        results['score'] = results['score'] == 1
        results['issue'] = results['issue'] == 1
    return results

def leagueForecastsResults():
    """
    returns the list of forecasts results for the mid and end of season
    """
    results = {}
    if midSeason():
        league_table = full_league_table_until(midSeasonWeek())
        results['winner_midseason'] = league_table[0][0] 
    if endOfSeason():
        league_table = full_league_table()
        results['winner'] = league_table[0][0]
        results['second'] = league_table[1][0]
        results['third'] = league_table[2][0]
        results['fourth'] = league_table[3][0]
        results['fifth'] = league_table[4][0]
        results['looser1'] = league_table[-1][0]
        results['looser2'] = league_table[-2][0]
        results['looser3'] = league_table[-3][0]
        results['looser4'] = league_table[-4][0]
    return results
        
def leagueForecastsResultsForPlayer(player):
    """
    get the list of league forecasts results for a player 
    """
    results = {}

    #get the league forecasts results    
    league_res = leagueForecastsResults()
    
    try:
        #get the league forecast for a player
        forecasts = LeagueForecast.objects.get(user__id=player)
        if forecasts:
        
            #verify all forecasts against results
            if 'winner_midseason' in league_res:
                results['winner_midseason']=(forecasts.winner_midseason.name == league_res['winner_midseason']) if forecasts.winner_midseason else False
            if 'winner' in league_res:
                results['winner']=(forecasts.winner.name == league_res['winner']) if forecasts.winner else False
            if 'second' in league_res:
                results['second']=(forecasts.second.name == league_res['second']) if forecasts.second else False
            if 'third' in league_res:
                results['third']=(forecasts.third.name == league_res['third']) if forecasts.third else False
            if 'fourth' in league_res:
                results['fourth']=(forecasts.fourth.name == league_res['fourth']) if forecasts.fourth else False
            if 'fifth' in league_res:
                results['fifth']=(forecasts.fifth.name == league_res['fifth']) if forecasts.fifth else False

            loosers = []
            for looser in ['looser1','looser2','looser3','looser4']:
                if looser in league_res:
                    loosers.append(league_res[looser])
            if loosers != []:
                results['looser1']=(forecasts.looser1.name in loosers) if forecasts.looser1 else False
                results['looser2']=(forecasts.looser2.name in loosers) if forecasts.looser2 else False
                results['looser3']=(forecasts.looser3.name in loosers) if forecasts.looser3 else False
                results['looser4'] = (forecasts.looser4.name in loosers) if forecasts.looser4 else False
    except LeagueForecast.DoesNotExist:
        pass
    
    return results

def getFixtureForecasts(fixture_id):
    """
    returns the list of forecasts for a given fixture
    ONLY if the fixture has started; otherwise returns empty list
    """
    if hasFixtureStarted(fixture_id):
        return Forecast.objects.filter(fixture__id=fixture_id)
        
    return []
    