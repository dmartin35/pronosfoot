"""
STATS MANAGEMENT
"""
import contextlib
from django.db.models.aggregates import Sum
from season.models import Table
from season.models import LeagueForecast
from season.queries import avg_goals_scored, best_stats, \
    convertToList, count_forecasts, count_forecasts_draw, count_forecasts_team_a_win, \
    count_forecasts_team_b_win, count_team_forecasts, count_team_forecasts_draw, \
    count_team_forecasts_lose, count_team_forecasts_win, goal_stats, \
    goals_scored_away, goals_scored_home, goals_taken_away, goals_taken_home, \
    issue_stats, less_goals_scored, matches_played, most_goals_scored, team_points, \
    team_win_draw_lose, total_goals_scored, users_stats, league_table_until_with_teamid, \
    user_total_until, user_table_until_week, user_table_with_bonus, user_total, \
    team_win_draw_lose_goals
from season.core.season import endOfSeason
from season.core.tables import team_played_weeks
from season.core.tables import played_weeks
from season.core.tables import TRENDS


__all__ = ['best_attack','best_defense','poorest_attack','poorest_defense',
           'most_victories','most_draws','most_losses',
           'less_victories','less_draws','less_losses',
           'team_trends','team_WDL','team_forecasts_trend',
           'forecasts_best_stats','fixture_forecasts_trend',
           'goals_scored_stats','team_goals_avg','team_points_avg',
           'team_points_evolution','team_pos_evolution',
           'player_points_evolution','player_pos_evolution',
           'player_points_per_week', 'team_points_per_week',
           'team_pos_evo_series'
           ]

def __extract_goal_stats_info(stats):
    try:
        number = stats[0][1]
        teams = [line[0] for line in stats]
        return (number, teams)
    except: 
        pass
    return (None,[])

def best_attack():
    stats = goal_stats('for', 'max')
    return __extract_goal_stats_info(stats)

def best_defense():
    stats = goal_stats('against', 'min')
    return __extract_goal_stats_info(stats)

def poorest_attack():
    stats = goal_stats('for', 'min')
    return __extract_goal_stats_info(stats)

def poorest_defense():
    stats = goal_stats('against', 'max')
    return __extract_goal_stats_info(stats)

def __extract_issue_stats_info(stats):
    try:
        number = stats[0][1]
        teams = [line[0] for line in stats]
        return (number, teams)
    except:
        pass
    return (None,[])

def most_victories():
    stats = issue_stats('win', 'max')
    return __extract_issue_stats_info(stats)

def most_draws():
    stats = issue_stats('draw', 'max')
    return __extract_issue_stats_info(stats)

def most_losses():
    stats = issue_stats('lose', 'max')
    return __extract_issue_stats_info(stats)

def less_victories():
    stats = issue_stats('win', 'min')
    return __extract_issue_stats_info(stats)

def less_draws():
    stats = issue_stats('draw', 'min')
    return __extract_issue_stats_info(stats)

def less_losses():
    stats = issue_stats('lose', 'min')
    return __extract_issue_stats_info(stats)

def __team_fixt_res_str(win,draw,lose):
    """
    returns the textual result of a team fixture, 
    given win/draw/lose boolean info of a match
    """
    return '%s%s%s' %('G' if win==1 else '', 
                     'N' if draw==1 else '', 
                     'P' if lose==1 else '')
    

def __extract_longest_trend(full_trend, patterns):
    """
    extract the longest string of valid patterns from the full_trend
    @param full_trend: a list of single char (G,N,P)
    @param patterns: a list of single char (G,N,P) to be extracted in the full form
    """
    longest = []
    current = []
    for val in full_trend:
        if val in patterns:
            current.append(val)
        else:
            if len(current)>len(longest):
                longest = current
            current = []
    if len(current)>len(longest):
        return current
    return longest

def team_trends(team_id):
    """
    returns a dictionary with different trend stats for a given team
    """
    trend = [__team_fixt_res_str(x.win,x.draw,x.lose) for x in Table.objects.filter(team=team_id,week__gt=0).order_by('week').all()]
    
    trends = {}
    trends['consecutive_wins'] = len(__extract_longest_trend(trend, ['G']))
    trends['consecutive_draws'] = len(__extract_longest_trend(trend, ['N']))
    trends['consecutive_losses'] = len(__extract_longest_trend(trend, ['P']))
    trends['consecutive_noloss'] = len(__extract_longest_trend(trend, ['G','N']))
    trends['consecutive_nowin'] = len(__extract_longest_trend(trend, ['P','N']))
    trends['last_five'] = trend[-5:]
    return trends

def team_WDL(team_id):
    """
    returns the number of Win/Draw/Lose fixtures 
    for a team for the entire season
    """
    wdl = list(team_win_draw_lose(team_id)[0])
    if wdl[0] or wdl[1] or wdl[2]:
        total = int(wdl[0]) + int(wdl[1]) + int(wdl[2])
        win =  100.0 * float(wdl[0]) / float(total)
        draw =  100.0 * float(wdl[1]) / float(total)
        lose =  100.0 * float(wdl[2]) / float(total)
        return ['%0.f'%win,'%0.f'%draw,'%0.f'%lose]
    return []

def team_wdl_goals(team_id):
    """
    returns the sums of Win/Draw/Lose/Goals for/Goals against
    for a team for the entire season 
    """
    counts = list(team_win_draw_lose_goals(team_id)[0])
    return {
        'won': counts[0],
        'drawn': counts[1],
        'lost': counts[2],
        'gf': counts[3],
        'ga': counts[4],
    }

def team_forecasts_trend(team_id):
    """
    return the percentage of win/draw/lose forecasts 
    for a team for the entire season
    """
    trends = {'team_forecasts_win':0,
              'team_forecasts_draw':0,
              'team_forecasts_lose':0,
              }
    
    total_forecasts = 0
    try:
        total_forecasts = int(convertToList(count_team_forecasts(team_id))[0])
    except:
        pass
    try:
        win_forecasts = int(convertToList(count_team_forecasts_win(team_id))[0])
        win_percentage = 100.0 * float(win_forecasts) / float(total_forecasts)
        trends['team_forecasts_win'] = '%0.f'%win_percentage
    except: 
        pass
    try:
        draw_forecasts = int(convertToList(count_team_forecasts_draw(team_id))[0])
        draw_percentage = 100.0 * float(draw_forecasts) / float(total_forecasts)
        trends['team_forecasts_draw'] = '%0.f'%draw_percentage
    except:
        pass
    try:
        lose_forecasts = int(convertToList(count_team_forecasts_lose(team_id))[0])
        lose_percentage = 100.0 * float(lose_forecasts) / float(total_forecasts)
        trends['team_forecasts_lose'] = '%0.f'%lose_percentage
    except: 
        pass
    
    return trends
    
def forecasts_best_stats():
    """
    returns the forecasts best stats of the season 
    """
    players_stats_res = users_stats()
    best_stats_res = best_stats()[0]

    forecasts_stats = {}
    for (idx, name) in [(0,'forecasts_best_points'),
                        (1,'forecasts_best_scores'),
                        (2,'forecasts_best_issues'),
                        ]:
        try:
            best_stat = best_stats_res[idx]
            best_players = []
            for player_stat_group in players_stats_res:
                player_stat = player_stat_group[(idx+1)]
                if player_stat == best_stat:
                    best_players.append(player_stat_group[0])
            #save best stat and list of players in result dict
            forecasts_stats[name] = {'value':best_stat,'players':best_players}
        except:
            pass
        
    return forecasts_stats
        
def fixture_forecasts_trend(fixture_id):
    """
    return the percentage of win/draw/lose forecasts for a fixture, 
    """
    trend = {}

    nb_forecasts = int(convertToList(count_forecasts(fixture_id))[0])
    
    nb_team_a_win = 0
    nb_team_b_win = 0
    nb_draw = 0
    
    if nb_forecasts > 0:
        nb_team_a_win = int(convertToList(count_forecasts_team_a_win(fixture_id))[0]) * 100 / nb_forecasts
        nb_team_b_win = int(convertToList(count_forecasts_team_b_win(fixture_id))[0]) * 100 / nb_forecasts
        nb_draw = int(convertToList(count_forecasts_draw(fixture_id))[0]) * 100 / nb_forecasts
    
    trend['nb_team_a_win'] = nb_team_a_win
    trend['nb_team_b_win'] = nb_team_b_win
    trend['nb_draw'] = nb_draw
    
    return trend

def goals_scored_stats():
    """
    returns the stats of goals scored for the season
    1. total of goals
    2. goal average by math
    3. biggest goals scored in one week
    4. lowest goals scored in one week
    """
    stats = {'most_goals':None,
             'less_goals':None,
             'total_goals':None,
             'avg_goals':None}
    
    for (var,query_cbk) in [('most_goals',most_goals_scored),
                            ('less_goals',less_goals_scored),
                            ('total_goals',total_goals_scored),
                            ('avg_goals',avg_goals_scored),
                            ]:
        try:
            stats[var] = query_cbk()[0][0]
        except:
            pass
    return stats

def team_goals_avg(team_id):
    """
    returns the average of goals scored and taken by a team
    """
    res = {'goals_scored_avg':0.0,'goals_taken_avg':0.0}
    played = 0
    try:
        played = matches_played(team_id)[0][0]
    except:
        pass
    try:
        scored = 0
        scored_home = goals_scored_home(team_id)[0][0]
        scored_away = goals_scored_away(team_id)[0][0]
        if not scored_home is None:
            scored += int(scored_home)
        if not scored_away is None:
            scored += int(scored_away)
        res['goals_scored_avg'] = float(scored)/float(played)
    except:
        pass
    try:
        taken = 0
        taken_home = goals_taken_home(team_id)[0][0]
        taken_away = goals_taken_away(team_id)[0][0]
        if not taken_home is None:
            taken += int(taken_home)
        if not taken_away is None:
            taken += int(taken_away)
        res['goals_taken_avg'] = float(taken)/float(played)
    except:
        pass
    return res

def team_points_avg(team_id):
    """
    returns the average of points earned by a team
    """
    avg = 0.0
    try:
        points = team_points(team_id)[0][0]
        played = matches_played(team_id)[0][0]
        avg = float(points)/float(played)
    except:
        pass
    return avg

def team_points_evolution(team_id):
    """
    returns the evolution of points 
    earned by a team for the season
    """
    pts_evo = []
    for week in team_played_weeks(team_id):
        try:
            pts = Table.objects.filter(team=team_id,week__gt=0,week__lte=week).order_by('week').aggregate(Sum('points'))['points__sum']
            pts_evo.append(pts)
        except:
            pass
    return pts_evo

def team_points_per_week(team_id):
    """
    returns the points per week
    earned by a team for the season
    """
    pts_weeks = []
    for week in team_played_weeks(team_id):
        try:
            pts = Table.objects.filter(team=team_id,week=week).order_by('week').aggregate(Sum('points'))['points__sum']
            pts_weeks.append(pts)
        except:
            pass
    return pts_weeks

def team_pos_evolution(team_id):
    """
    returns the evolution of position 
    for a team for the season
    """
    pos_evo = []
    for week in team_played_weeks(team_id):
        try:
            teams_pos = [x[0] for x in league_table_until_with_teamid(week)]
            pos = teams_pos.index(int(team_id)) + 1
            pos_evo.append(pos)
        except:
            pass
    return pos_evo


WDL_COLORS = {'win': '#8bc34a', 'draw': '#adadad', 'lose': '#D3423D'}


def team_pos_evo_series(team_id):
    """
    Returns the evolution of the position for the team, 
    with the color for the related fixture WDL result,
    for each match day
    :param team_id: 
    :return: json
    """
    series = []
    for week in team_played_weeks(team_id):
        with contextlib.suppress(Exception):
            day_pos = Table.objects.get(team=team_id, week=week)
            fixture_result = TRENDS.get((day_pos.win, day_pos.draw, day_pos.lose))
            table_until = league_table_until_with_teamid(week)
            team_ids = [x[0] for x in table_until]
            position = team_ids.index(int(team_id)) + 1

            point = {
                'x': week,
                'y': position,
                'color': WDL_COLORS.get(fixture_result)
            }
            series.append(point)
    return series


def player_points_evolution(player_id):
    """
    returns the evolution of points 
    earned by a player for the season
    """
    pts_evo = []
    for week in played_weeks():
        try:
            pts = int(user_total_until(player_id,week)[0][0])
            pts_evo.append(pts)
        except:
            pass
    try:
        if endOfSeason():
            #in case of season end, need to add bonus points to last week points
            bonus = LeagueForecast.objects.get(user__id=player_id).points
            pts_evo[len(pts_evo)-1] = pts_evo[len(pts_evo)-1] + bonus
    except:
        pass
    return pts_evo

def player_points_per_week(player_id):
    """
    returns the points per week
    earned by a player for the season
    """
    pts_weeks = []
    for week in played_weeks():
        try:
            pts = int(user_total(player_id,week)[0][0])
            pts_weeks.append(pts)
        except:
            pass
    try:
        if endOfSeason():
            #in case of season end, need to add bonus points to last week points
            bonus = LeagueForecast.objects.get(user__id=player_id).points
            pts_weeks[len(pts_weeks)-1] += bonus
    except:
        pass
    return pts_weeks

def player_pos_evolution(player_id):
    """
    returns the evolution of position 
    for a player for the season
    """
    pos_evo = []
    weeks = played_weeks()
    eos = endOfSeason()
    last_week = weeks[-1]
    for week in weeks:
        try:
            user_table = user_table_until_week(week) 
            #in case of last week - and end of season - need to use
            #table with bonuses instead on simple table
            if eos and week == last_week:
                user_table = user_table_with_bonus()
            players_pos = [x[0] for x in user_table]
            pos = players_pos.index(int(player_id)) + 1
            pos_evo.append(pos)
        except:
            pass
    return pos_evo