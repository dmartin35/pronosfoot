from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
import json

from django.contrib.auth.views import login as djangologin
from django.contrib.auth import login as djangologin_user

from django.conf import settings
from django import http
from django.template import Context, loader

from season.models import Player
from season.models import Mailing
from auth.forms import UserCreationForm
# from auth.decorators import ajax_login_required
# from auth.decorators import ajax_logged_in
from tools.utils import evo_progress

#SEASON IMPORTS
from season.core.season import endOfSeason
#WEEKS IMPORTS
from season.core.weeks import getWeekAuto
from season.core.weeks import WEEK_CLOSEST
from season.core.weeks import isWeekValid
from season.core.weeks import getAllWeeks
#FIXTURES IMPORTS
from season.core.fixtures import fixtures as fixturesList
from season.core.fixtures import fixturesDays
from season.core.fixtures import fixturesDaysAndWeeksForMonth
from season.core.fixtures import fixtureTeams
from season.core.fixtures import isFixtureValid
from season.core.fixtures import hasFixtureStarted
from season.core.fixtures import getFixture
#CALENDAR IMPORTS
from tools.cal import monthcal
from tools.cal import previous_month
from tools.cal import next_month
#FORECASTS IMPORTS
from season.core.forecasts import saveForecastsFormset
from season.core.forecasts import getForecastsFormset
from season.core.forecasts import saveLeagueForecastsForm
from season.core.forecasts import getLeagueForecastsForm
from season.core.forecasts import countForecastsForMonth
from season.core.forecasts import mergeForecastFormsetAdditionalInfo
from season.core.forecasts import forecastsTotalPointsForWeek
from season.core.forecasts import forecastResult
from season.core.forecasts import leagueForecastsResults
from season.core.forecasts import leagueForecastsResultsForPlayer
from season.core.forecasts import getFixtureForecasts
#TABLES IMPORTS
from season.core.tables import last_played_week
from season.core.tables import played_weeks
from season.core.tables import full_league_table_until__dict
from season.core.tables import full_players_table_for_week
from season.core.tables import full_players_table_with_bonus
from season.core.tables import full_players_table_until_auto
from season.core.tables import team_played_weeks
#STATS IMPORTS
from season.core.stats import best_attack
from season.core.stats import best_defense
from season.core.stats import poorest_attack
from season.core.stats import poorest_defense
from season.core.stats import most_victories
from season.core.stats import most_draws
from season.core.stats import most_losses
from season.core.stats import less_victories
from season.core.stats import less_draws
from season.core.stats import less_losses
from season.core.stats import team_trends
from season.core.stats import team_WDL
from season.core.stats import team_wdl_goals
from season.core.stats import team_forecasts_trend
from season.core.stats import forecasts_best_stats
from season.core.stats import fixture_forecasts_trend
from season.core.stats import goals_scored_stats
from season.core.stats import team_goals_avg
from season.core.stats import team_points_avg
from season.core.stats import team_points_evolution
from season.core.stats import team_pos_evolution
from season.core.stats import team_points_per_week
from season.core.stats import player_points_evolution
from season.core.stats import player_pos_evolution
from season.core.stats import player_points_per_week
from season.core.stats import team_pos_evo_series
#TEAMS IMPORT
from season.core.teams import firstAvailableTeam
from season.core.teams import isTeamValid
from season.core.teams import getAllTeams
from season.core.teams import getTeamName
#PLAYER IMPORT
from season.core.player import isPlayerValid
from season.core.player import getAllPlayers
from season.core.player import getPlayerName

import datetime
import uuid
import re

def _validGetRequest(request):
    """
    check the given request has been sent using GET method
    """
    if request.method == 'GET':
        return True
    else:
        return False


def _validPostRequest(request):
    """
    check the given request has been sent using POST method
    """
    if request.method == 'POST':
        return True
    else:
        return False


def _validAjaxRequest(request):
    """
    check the given request has been sent using AJAX
    """
    if request.is_ajax():
        return True
    else:
        return False

# def server_error(request, template_name='500.html'):
#     """
#     500 error handler.
#
#     Templates: `500.html`
#     Context:
#         MEDIA_URL
#             Path of static media (e.g. "media.example.org")
#     """
#     t = loader.get_template(template_name) # You need to create a 500.html template.
#     return http.HttpResponseServerError(t.render(Context({
#         'MEDIA_URL': settings.MEDIA_URL,
#         'RootUrl': settings.ROOT_URL
#     })))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            
            #save new user in players table
            new_player = Player(id=new_user.id, name=new_user.username)
            new_player.save()
            #initializes the mailing options the new user
            mailing = Mailing(user_id=new_user.id,
                              newsletter=True, reminder=True,
                              news_key=str(uuid.uuid1()),
                              remind_key=str(uuid.uuid1()))
            mailing.save()
            
            #authenticate and auto log in new user
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            djangologin_user(request, user)
            request.session['_auth_user_id'] = user.id

            return redirect('index')
    else:
        form = UserCreationForm()
    return TemplateResponse(request, 'registration/register.html', {'form': form})
    # return render(request, 'registration/register.html', {'form': form})


# #@ajax_logged_in
# def login(request):
#     """
#     should get here after POST sent from ajax login lightbox
#     """
#     if not _validAjaxRequest(request):
#         return HttpResponse(status=400)
#     if not _validPostRequest(request):
#         return HttpResponse(status=400)
#
#     return djangologin(request)


def index(request):
    """
    render the home page
    """
    #ad info to context - to be passed to templates -
    context = {'selectedmenu':'home', 'page_title': _('Home'),}
    return render(request, 'pages/home.html', context)


def fixtures(request, week):
    """
    render the fixtures full page
    """
    #get closest week from today's date
    today = datetime.datetime.now().strftime(settings.DATE_FORMAT)

    if week:
        if not isWeekValid(week):
            raise Http404
        else:
            week = int(week)

    week = week or getWeekAuto(today, WEEK_CLOSEST)

    #list of days for all fixtures of the week 
    days = fixturesDays(week)
    
    #get calendar context - for first day of the week's fixtures
    firstday = days[0]
    
    #get previous and next month 
    (prev_y,prev_m) = previous_month(firstday.year, firstday.month)
    (next_y,next_m) = next_month(firstday.year, firstday.month)

    #ad info to context - to be passed to templates -
    context = {'selectedmenu':'fixtures',
               'page_title': _('Fixtures'),
               'currentweek':week,
               'weeks':getAllWeeks(), 
               'fixtures':fixturesList(week),
               'days':days, 
               'season':settings.SEASON,
               'calendar':monthcal(firstday.year, firstday.month),
               'current_month': datetime.date(firstday.year,firstday.month,1),
               'prev_year':prev_y,'prev_month':prev_m,
               'next_year':next_y,'next_month':next_m,
               'day_to_week':fixturesDaysAndWeeksForMonth(firstday.year, firstday.month),
               }

    #get player forecasts count for calendar
    if request.user.is_authenticated():
        context['forecasts_cal'] = countForecastsForMonth(firstday.year, firstday.month, request.user.id)
    
    return render(request, 'pages/matches.html',context)

    
def ajax_fixtures(request,week):
    """
    returns the fixtures section for the required week
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)
    
    if not isWeekValid(week):
        return HttpResponse(status=400)
    
    #ad info to context - to be passed to templates -
    context = {'currentweek':week, 
               'weeks':getAllWeeks(), 
               'fixtures':fixturesList(week),
               'days':fixturesDays(week), 
               'season':settings.SEASON
               }
    
    return render(request, 'contents/fixtures.html',context)
    

@login_required
def forecasts(request,week):
    """
    render the forecasts full page
    """
    #get the current time - time of forecast page request
    requesttime = datetime.datetime.now()
    
    #check week validity
    if not isWeekValid(week):
        #get next week from today's date
        today = requesttime.strftime(settings.DATE_FORMAT)
        week = getWeekAuto(today, WEEK_CLOSEST)
    else:
        week = int(week)
        
    #ad info to context - to be passed to templates -
    context = {'selectedmenu':'forecasts',
               'page_title': _('Forecasts'),
               'currentweek':week,
               'weeks':getAllWeeks(),
               'days':fixturesDays(week),
               'ff_formset':getForecastsFormset(week, request.user.id), 
               'ff_saved':False,
               'week_points':forecastsTotalPointsForWeek(week, request.user.id),
               'season':settings.SEASON,
               'fl_form':getLeagueForecastsForm(request.user.id),
               'fl_saved':False,
               'fl_vote_date':settings.SEASON_FORECAST_MAX_DATE,
               'fl_res':leagueForecastsResultsForPlayer(request.user.id),
               'fl_res_teams':leagueForecastsResults(),
               }
            
    return render(request, 'pages/pronos.html',context)


#@ajax_login_required
def ajax_forecasts_fixtures(request, week):
    """
    validate/save the forecasts from POST request
    and return the forecast form section 
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    
    #try to save the formset (on POST)- formset with errors will be return in validation error
    (saved,errorformset) = saveForecastsFormset(request)
    
    #get clean formset for week     
    formset = getForecastsFormset(week, request.user.id)
    
    #if errors while saving formset submitted, add submitted data 
    #to clean formset and errors
    if not errorformset is None:
        formset = mergeForecastFormsetAdditionalInfo(formset,errorformset)
         
    #ad info to context - to be passed to templates -
    context = {'currentweek':week,
               'days':fixturesDays(week),
               'ff_saved':saved,
               'ff_formset': formset,
               'week_points':forecastsTotalPointsForWeek(week, request.user.id),
               }
    
    return render(request, 'contents/pronos_matches.html',context)

    
#@ajax_login_required
def ajax_forecasts_league(request):
    """
    validate/save the forecasts from POST request
    and return the forecast form section 
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    
    #try to save the form (on POST)- form with errors will be return in validation error
    (saved,errorform) = saveLeagueForecastsForm(request)
    
    #ad info to context - to be passed to templates -
    context = {#save forecasts form - if post request -
               'fl_saved':saved,
               #in case of error form, use error form, otherwise
               #get form for current player - need to be called after form save, 
               #to have saved value returned in the next form
               'fl_form':errorform if not saved and errorform else getLeagueForecastsForm(request.user.id),
               'fl_res':leagueForecastsResultsForPlayer(request.user.id),
               }
    
    return render(request, 'contents/pronos_saison.html', context)

    
def tables(request):
    """
    render the tables full page
    """
    #get last played week available for league table
    currentweek = last_played_week()

    #end of season boolean
    eos = endOfSeason()
    
    #ad info to context - to be passed to templates -
    context = {'selectedmenu':'tables',
               'page_title': _('Tables'),
               'season':settings.SEASON,
               'currentweek':currentweek,
               'weeks':played_weeks(),
               'league_table': full_league_table_until__dict(currentweek),
               'eos':eos,
               'players_table':full_players_table_until_auto() if not eos else full_players_table_with_bonus(),
               'final_players_table':eos,
               }
    
    return render(request, 'pages/classements.html', context)


def ajax_league_table(request,week):
    """
    returns the full league until the specified week 
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)
    
    try:
        week = int(week)
    except:
        return HttpResponse(status=400)
     
    if not week in played_weeks():
        return HttpResponse(status=400)
    
    #ad info to context - to be passed to templates -
    context = {'league_table': full_league_table_until__dict(week),
               }
    
    return render(request, 'contents/classement_league.html', context)


def ajax_players_table(request,week):
    """
    returns the players table for the specified week
    if week is None, returns the full table for all played weeks 
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)
    
    #if week is given, check validity
    if not week is None:
        try:
            week = int(week)
        except:
            return HttpResponse(status=400)
     
        if not week in played_weeks():
            return HttpResponse(status=400)
        
    #end of season boolean
    eos = endOfSeason()
        
    #players table, if week, table for given week
    #else full season table - depending on end of season -
    players_table = None
    if not week is None:
        players_table = full_players_table_for_week(week)
    else:
        players_table = full_players_table_until_auto() if not eos else full_players_table_with_bonus()
    
    #ad info to context - to be passed to templates -
    context = {'eos':eos,
               'players_table': players_table,
               'final_players_table': eos and week is None,  
               }
    
    return render(request, 'contents/classement_pronos.html', context)


def stats(request):
    """
    render the stats full page
    """
    #get trends for first team available
    team = firstAvailableTeam()
    
    #ad info to context - to be passed to templates -
    context = {'selectedmenu':'statistics',
               'page_title': _('Statistics'),
               'best_attack':best_attack(),
               'best_defense':best_defense(),
               'poorest_attack':poorest_attack(),
               'poorest_defense':poorest_defense(),
               'most_victories':most_victories(),
               'most_draws':most_draws(),
               'most_losses':most_losses(),
               'less_victories':less_victories(),
               'less_draws':less_draws(),
               'less_losses':less_losses(),
               'teams':getAllTeams(),
               'w_d_l':team_WDL(team.id),
               'team_wdl_goals': team_wdl_goals(team.id),
               'weeks':getAllWeeks(),
               'team_name':team.name,
               'pts_avg':team_points_avg(team.id),
               }
    context.update(team_trends(team.id))
    context.update(team_forecasts_trend(team.id))
    context.update(team_goals_avg(team.id))
    context.update(forecasts_best_stats())
    context.update(goals_scored_stats())
    
    return render(request, 'pages/stats.html', context)


def unsubscribe(request, type, infos):
    """
    generic method to submit user unsubscription
    for a mailing system: newsletter, reminder, etc.
    
    @param type: the element the user wants to unsubscribe from
    @param infos: the entire URL params 
    """
    fields = {'newsletter':{'field':'newsletter','token':'news_key'},
              'reminder':{'field':'reminder','token':'remind_key'}}
    
    if type not in list(fields.keys()):
        raise Http404
    
    if infos is None or infos == '':
        raise Http404
    
    (user, email, token) = _parse_unsubscribe_infos(infos)
    
    if ( (user is None) or (email is None) or (token is None) ):
        raise Http404
        
    #find user by its username
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        user = None
    if not user:
        raise Http404
    
    #check the user email matches
    if user.email != email:
        raise Http404
    
    #get the associated mailing line
    mailing = Mailing.objects.get(user=user)
    if not mailing:
        raise Http404
    
    registered_token = getattr(mailing, fields[type]['token'])
    
    #check token matches
    if ( (registered_token is None) or 
         (registered_token == '') or
         (registered_token != token) ):
            raise Http404
    
    #unsubscribe user for the right element and remove token
    setattr(mailing, fields[type]['field'], False)
    setattr(mailing, fields[type]['token'], None)
    mailing.save()
    
    return render(request, 'unsubscription/%s.html'%type)


def _parse_unsubscribe_infos(infos):
    """
    parse the unsubscription info given in the URL
    to return the username, user email, and unsubscription token 
    """
    pattern = '(?P<user>.*?)-(?P<email>.*?)-(?P<token>.*)$'
    match = re.search(pattern, infos, re.DOTALL)
    if match:
        return (match.group('user'), 
                match.group('email'),
                match.group('token')
                )
    return (None, None, None)


def ajax_calendar(request,year,month):
    """
    returns the calendar section for a given year/month 
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)
    
    year = int(year)
    month = int(month)
    
    #prepare previous and next month links info
    (prev_y,prev_m) = previous_month(year, month)
    (next_y,next_m) = next_month(year, month)
            
    #ad info to context - to be passed to templates -
    context = {'calendar':monthcal(year, month),
               'current_month': datetime.date(year,month,1),
               'prev_year':prev_y,'prev_month':prev_m,
               'next_year':next_y,'next_month':next_m,
               'day_to_week':fixturesDaysAndWeeksForMonth(year,month),
               }
    
    #get player forecasts count for calendar
    if request.user.is_authenticated():
        context['forecasts_cal'] = countForecastsForMonth(year, month, request.user.id)
    
    return render(request, 'contents/calendar.html',context)

    
# def ajax_login(request,redirect):
#     """
#     returns the login page
#     """
#     #ad info to context - to be passed to templates -
#     context = {'next':redirect if redirect in ['matches','pronos','classements','stats'] else ''}
#     return render(request, 'registration/login.html', context)
#
#
# def ajax_register(request):
#     """
#     returns the registration page
#     """
#     return render(request, 'registration/register.html')


# def ajax_timeout(request):
#     """
#     returns the time out page
#     """
#     return render(request, 'lightboxes/timeout.html')
#
#
# def ajax_need_login(request):
#     """
#     returns the need login page
#     """
#     return render(request, 'lightboxes/needlogin.html')


def ajax_stats_team(request,team_id):
    """
    returns the team statistics section for the required team_id 
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)
    
    if not isTeamValid(team_id):
        return HttpResponse(status=400)
    
    #ad info to context - to be passed to templates -
    context = {'w_d_l':team_WDL(team_id),
               'team_wdl_goals': team_wdl_goals(team_id),
               'team_name':getTeamName(team_id),
               'pts_avg':team_points_avg(team_id),
               }
    context.update(team_trends(team_id))
    context.update(team_forecasts_trend(team_id))
    context.update(team_goals_avg(team_id))
    
    return render(request, 'contents/stats_team.html', context)


# def ajax_players_forecasts_for_fixture(request,fixture_id):
#     """
#     returns the list of forecasts, for all players,
#     for a given fixture; only if fixture has started
#     Avoid seeing other player's forecast, when modification is alowed
#     """
#     if not _validAjaxRequest(request):
#         return HttpResponse(status=400)
#     if not _validGetRequest(request):
#         return HttpResponse(status=400)
#
#     if not isFixtureValid(fixture_id):
#         return HttpResponse(status=400)
#
#     context = {'players_forecasts':getFixtureForecasts(fixture_id),
#                'trend_forecasts':fixture_forecasts_trend(fixture_id),
#                'fixture_teams':fixtureTeams(fixture_id),
#                'fixture_started':hasFixtureStarted(fixture_id),
#                }
#     return render(request, 'lightboxes/forecast_stats.html',context)


def ajax_forecasts_trends_for_week(request, week):
    """
    returns the html popup code of the forecast trends 
    for each fixture of the week
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)

    #get the list of fixture of the week
    fixtures = fixturesList(week)
    
    week_trends = {}
    for fixture in fixtures:
        #get the forecasts trend for the current fixture
        trend_ctx = fixture_forecasts_trend(fixture.id)
        #get the team names
        trend_ctx.update(fixtureTeams(fixture.id))
        #get the trend template for the current fixture
        t = loader.get_template('global/forecasts_trend.html')
        c = Context(trend_ctx)
        tplstring = t.render(c).replace('\n','')
        #add the current trend h(tml code)
        #to weeks trend dict to be returned
        week_trends[fixture.id] = tplstring

    return JsonResponse(week_trends)

def ajax_forecast_trend_fixture(request, fixture_id):
    """
    Returns the trend of forecast for a specific fixture, for all players - for graph
    If the match is started, also returns the list of forecasts for each player - for comparison
    If the match is over, returns the fixture result - for final score display
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)

    fixture = getFixture(fixture_id)
    if not fixture:
        return HttpResponse(status=400)

    fixture.is_started = hasFixtureStarted(fixture_id)
    trend = fixture_forecasts_trend(fixture_id)
    # series = [{
    #     'name': 'Victoire  de {}'.format(fixture.team_b),
    #     'data': trend.get('nb_team_b_win', 0),
    #     'color': '#D3423D',
    # }, {
    #     'name': 'Match nul',
    #     'data': trend.get('nb_draw', 0),
    #     'color': '#adadad',
    # }, {
    #     'name': 'Victoire  de {}'.format(fixture.team_a),
    #     'data': trend.get('nb_team_a_win', 0),
    #     'color': '#8bc34a',
    # }]

    context = {
        'trend': trend,
        'forecasts': getFixtureForecasts(fixture_id),
        'fixture': fixture,
        # 'trend_chart': series,
    }

    return render(request, 'snippets/forecast_details.html', context)


#@ajax_login_required
def ajax_forecasts_results(request, week):
    """
    returns the html popup code for all forecasts results 
    for fixture of the week
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)
    
    #get the list of fixture of the week
    fixtures = fixturesList(week)
    
    week_results = {}
    for fixture in fixtures:
        #get the forecast result
        res_ctx = forecastResult(fixture.id,request.user.id)
        if not res_ctx['points'] is None:
            #add fixture score result to ctx
            res_ctx['score_a'] = fixture.score_a
            res_ctx['score_b'] = fixture.score_b
            #get the  template for the current forecast result
            t = loader.get_template('global/forecast_result.html')
            c = Context(res_ctx)
            tplstring = t.render(c).replace('\n','')
            #add the current trend h(tml code)
            #to weeks trend dict to be returned
            week_results[fixture.id] = tplstring

    return JsonResponse(week_results)

def ajax_forecasts_league_results(request):
    """
    returns the html popup code for all league forecasts results 
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)
    
    res = {}
    league_res = leagueForecastsResults()
    for (title,team) in list(league_res.items()):
        teams = [team]
        if 'looser' in title:
            teams = [league_res['looser%d'%idx] for idx in range(1,4) if 'looser%d'%idx in league_res]
        #get the  template for the current forecast result
        t = loader.get_template('global/forecast_league_result.html')
        c = Context({'title':title,'teams':teams})
        tplstring = t.render(c).replace('\n','')
        #add the current info (html code)
        #to res dict to be returned
        res[title] = tplstring

    return JsonResponse(res)
#
# def ajax_evo_team(request, team_id):
#     """
#     returns the evolution of the position,
#     progression and points
#     for a team for the season
#     """
#     if not _validAjaxRequest(request):
#         return HttpResponse(status=400)
#     if not _validGetRequest(request):
#         return HttpResponse(status=400)
#
#     if not isTeamValid(team_id):
#         return HttpResponse(status=400)
#
#     pos = team_pos_evolution(team_id)
#     #ad info to context - to be passed to templates -
#     context = {'evo_weeks':team_played_weeks(team_id),
#                'evo_pos':pos,
#                'evo_progress':evo_progress(pos),
#                'evo_points':team_points_evolution(team_id),
#                'evo_pts_per_week':team_points_per_week(team_id),
#                'evo_name':getTeamName(team_id),
#                'evo_nb_max':len(getAllTeams()),
#                'chart_pts_tickInterval': 10,
#                'chart_pos_tickInterval': 5,
#                'chart_pos_minorTickInterval': 1,
#                }
#
#     return render(request, 'lightboxes/evo.html',context)



def ajax_evo_team(request, team_id):
    """
    returns the evolution of the position, 
    progression and points 
    for a team for the season
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)
    if not isTeamValid(team_id):
        return HttpResponse(status=400)

    # ad info to context - to be passed to templates -
    context = {'evo_weeks': team_played_weeks(team_id),
               'evo_pos': team_pos_evo_series(team_id),
               'team_id': team_id,
               'team_name': getTeamName(team_id),
               }
    return JsonResponse(context)


def ajax_evo_player(request, player_id):
    """
    returns the evolution of the position, 
    progression and points 
    for a player for the season
    """
    if not _validAjaxRequest(request):
        return HttpResponse(status=400)
    if not _validGetRequest(request):
        return HttpResponse(status=400)
    if not isPlayerValid(player_id):
        return HttpResponse(status=400)
    
    #ad info to context - to be passed to templates -
    context = {'evo_weeks':played_weeks(),
               'evo_pos':player_pos_evolution(player_id),
               #'evo_progress':evo_progress(pos),
               #'evo_points':player_points_evolution(player_id),
               #'evo_pts_per_week':player_points_per_week(player_id),
               'player_id': player_id,
               'player_name':getPlayerName(player_id),
               'nb_players':len(getAllPlayers()),
               #'chart_pts_tickInterval': 25,
               #'chart_pos_tickInterval': 1,
               #'chart_pos_minorTickInterval': 0,
               }
    return JsonResponse(context)
    #return render(request, 'lightboxes/evo.html', context)

