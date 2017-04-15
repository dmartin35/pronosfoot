"""
Models API - requests with models
"""
from tools.djangodb import executeRawSqlQuery

def convertToList(tuplelist):
    """
    convert a list of tuples with single values to a list of values
    """
    res = []
    for elem in tuplelist:
        res.append(elem[0])
    return res

def user_table():
    request = """
    SELECT season_player.id,
           season_player.name,
           sum(points) as points, 
           sum(score) as scores, 
           sum(issue) as issues, 
           count(points) as matches
    FROM season_forecast
    INNER JOIN season_player
    ON season_forecast.user_id = season_player.id
    GROUP BY season_player.id, season_player.name
    HAVING count(points) > 0
    ORDER BY points DESC, scores DESC, 
             issues DESC, matches, season_player.name    
    """
    return executeRawSqlQuery(request)

def user_table_for_week(week):
    request = """
    SELECT season_player.id,
           season_player.name,
           sum(points) as points, 
           sum(score) as scores, 
           sum(issue) as issues,
           count(points) as matches           
    FROM season_forecast
    INNER JOIN season_fixture
    ON season_forecast.fixture_id = season_fixture.id
    INNER JOIN season_player
    ON season_forecast.user_id = season_player.id
    WHERE week = '%s'
    GROUP BY season_player.id, season_player.name
    HAVING count(points) > 0
    ORDER BY points DESC, scores DESC, 
             issues DESC, matches, season_player.name
    """%(week)
    return executeRawSqlQuery(request)

def user_table_until_week(week):
    request = """
    SELECT season_player.id,
           season_player.name,
           sum(points) as points, 
           sum(score) as scores, 
           sum(issue) as issues,
           count(points) as matches           
    FROM season_forecast
    INNER JOIN season_fixture
    ON season_forecast.fixture_id = season_fixture.id
    INNER JOIN season_player
    ON season_forecast.user_id = season_player.id
    WHERE week <= '%s'
    GROUP BY season_player.id, season_player.name
    HAVING count(points) > 0
    ORDER BY points DESC, scores DESC, 
             issues DESC, matches, season_player.name
    """%(week)
    return executeRawSqlQuery(request)

def user_result(week, user):
    request = """
    SELECT season_forecast.fixture_id,
           season_forecast.score_a, season_forecast.score_b,
           season_forecast.score, season_forecast.issue,
           season_forecast.points  
    FROM season_forecast
    INNER JOIN season_fixture
    ON season_forecast.fixture_id = season_fixture.id
    INNER JOIN season_player
    ON season_forecast.user_id = season_player.id
    WHERE season_forecast.user_id = '%s' AND week = '%s'
    ORDER BY season_fixture.day, season_fixture.hour
    """ % (user, week)
    return executeRawSqlQuery(request)

class Result:
    def __init__(self):
        self.fixture_id = None
        self.prono_a = None
        self.prono_b = None
        self.score = None
        self.issue = None
        self.points = None
        
def convertToResultList(tuplelist):
    """
    convert a list of tuples to a list of Result objects
    """
    res = []
    for elem in tuplelist:
        result = Result()
        result.fixture_id = elem[0]
        result.prono_a = elem[1]
        result.prono_b = elem[2]
        result.score = elem[3]
        result.issue = elem[4]
        result.points = elem[5]
        res.append(result)
    return res

def user_total(user, week):
    request = """
    SELECT sum(points) as total
    FROM season_forecast
    INNER JOIN season_fixture
    ON season_forecast.fixture_id = season_fixture.id
    WHERE season_forecast.user_id = '%s' AND week = '%s'
    """ % (user, week)
    return executeRawSqlQuery(request)

def user_total_until(user, week):
    request = """
    SELECT sum(points) as total
    FROM season_forecast
    INNER JOIN season_fixture
    ON season_forecast.fixture_id = season_fixture.id
    WHERE season_forecast.user_id = '%s' AND week <= '%s'
    """ % (user, week)
    return executeRawSqlQuery(request)

def users_stats():
    request = """
    SELECT player, 
    max(points) as maxpoints, 
    max(scores) as maxscores, 
    max(issues) as maxissues
    FROM(

        SELECT season_player.name as player, 
        sum(points) as points,
        sum(score) as scores,
        sum(issue) as issues
        FROM season_forecast
        INNER JOIN season_fixture
        ON season_forecast.fixture_id = season_fixture.id
        INNER JOIN season_player
        ON season_forecast.user_id = season_player.id    
        GROUP BY season_player.name, week

    ) maxpoints
    GROUP BY player
    """
    return executeRawSqlQuery(request)

def best_stats():
    request = """    
    SELECT 
    max(points) as maxpoints, 
    max(scores) as maxscores, 
    max(issues) as maxissues
    FROM(

        SELECT season_forecast.user_id as player, 
        sum(points) as points,
        sum(score) as scores,
        sum(issue) as issues
        FROM season_forecast
        INNER JOIN season_fixture
        ON season_forecast.fixture_id = season_fixture.id    
        GROUP BY season_forecast.user_id, week

    ) maxpoints
    """
    return executeRawSqlQuery(request)

def count_forecasts(fixture_id):
    request = """
    SELECT COUNT(*)
    FROM season_forecast, season_fixture
    WHERE season_forecast.fixture_id = season_fixture.id
    AND season_fixture.id = '%s'
    AND season_forecast.score_a IS NOT NULL
    AND season_forecast.score_b IS NOT NULL
    """ % (fixture_id)
    return executeRawSqlQuery(request)

def count_forecasts_team_a_win(fixture_id):
    request = """
    SELECT COUNT(*)
    FROM season_forecast, season_fixture
    WHERE season_forecast.fixture_id = season_fixture.id
    AND season_fixture.id = '%s'
    AND season_forecast.score_a > season_forecast.score_b
    """ % (fixture_id)
    return executeRawSqlQuery(request)

def count_forecasts_team_b_win(fixture_id):
    request = """
    SELECT COUNT(*)
    FROM season_forecast, season_fixture
    WHERE season_forecast.fixture_id = season_fixture.id
    AND season_fixture.id = '%s'
    AND season_forecast.score_a < season_forecast.score_b
    """ % (fixture_id)
    return executeRawSqlQuery(request)

def count_forecasts_draw(fixture_id):
    request = """
    SELECT COUNT(*)
    FROM season_forecast, season_fixture
    WHERE season_forecast.fixture_id = season_fixture.id
    AND season_fixture.id = '%s'
    AND season_forecast.score_a = season_forecast.score_b
    """ % (fixture_id)
    return executeRawSqlQuery(request)

def goal_stats(goalmode,minmax):
    """
    to get either best attack or best defense 
    or poorest attack or poorest defense
    
    goalmode: for | against
    minmax: min | max
    """
    request = """
    SELECT * from (
        SELECT season_team.name AS team, 
        sum(goal_%(goalmode)s) AS goal_%(goalmode)s
        FROM season_team, season_table
        WHERE season_team.id = season_table.team_id
        AND week > 0    
        GROUP BY season_team.name
    )innertable
    WHERE goal_%(goalmode)s = (
        SELECT %(minmax)s(goal_%(goalmode)s) 
        FROM (
            SELECT season_team.name AS team, 
            sum(goal_%(goalmode)s) AS goal_%(goalmode)s
            FROM season_team, season_table
            WHERE season_team.id = season_table.team_id
            AND week > 0
            GROUP BY season_team.name
            )innertable
    )
    """ % ({'goalmode':goalmode,'minmax':minmax}) 
    return executeRawSqlQuery(request)
    
def issue_stats(issue,minmax):
    """
    to get min/max numbers of fixtures issues: win, draw, loose
    for the entire season
    issue: win | draw | lose
    minmax: min | max
    """
    request = """
    SELECT * from (
        SELECT season_team.name AS team, 
        count(%(issue)s) AS %(issue)s
        FROM season_team, season_table
        WHERE season_team.id = season_table.team_id
        AND %(issue)s > 0
        AND week > 0
        GROUP BY season_team.name
    )innertable
    WHERE %(issue)s = (
        SELECT %(minmax)s(%(issue)s) 
        FROM (
            SELECT season_team.name AS team, 
            count(%(issue)s) AS %(issue)s
            FROM season_team, season_table
            WHERE season_team.id = season_table.team_id
            AND %(issue)s > 0
            AND week > 0
            GROUP BY season_team.name
            )innertable
    )
    """ % ({'issue': issue, 'minmax': minmax})
    return executeRawSqlQuery(request)

def team_win_draw_lose(team_id):
    """
    return the number of win, draw, lose 
    for the given team for the entire season
    """
    request = """
    SELECT sum(win), sum(draw), sum(lose)
    FROM season_table
    WHERE team_id = '%s'
    """ % (team_id)
    return executeRawSqlQuery(request)

def count_team_forecasts(team_id):
    """
    count the number of forecasts for a team
    """
    request = """
    SELECT COUNT(*)
    FROM season_forecast, season_fixture
    WHERE season_forecast.fixture_id = season_fixture.id
    AND (
    season_fixture.team_a_id = '%(team_id)s'
    OR season_fixture.team_b_id = '%(team_id)s'
    )
    """ % ({'team_id':team_id})
    return executeRawSqlQuery(request)

def count_team_forecasts_win(team_id):
    """
    count the number of win forecasts for a team 
    """
    request = """
    SELECT COUNT(*)
    FROM season_forecast, season_fixture
    WHERE season_forecast.fixture_id = season_fixture.id
    AND (
     (season_fixture.team_a_id = '%(team_id)s' AND season_forecast.score_a > season_forecast.score_b) 
    OR (season_fixture.team_b_id = '%(team_id)s' AND season_forecast.score_a < season_forecast.score_b)
    )
    """ % ({'team_id':team_id})
    return executeRawSqlQuery(request)    

def count_team_forecasts_draw(team_id):
    """
    count the number of draw forecasts for a team
    """
    request = """
    SELECT COUNT(*)
    FROM season_forecast, season_fixture
    WHERE season_forecast.fixture_id = season_fixture.id
    AND (
     (season_fixture.team_a_id = '%(team_id)s' AND season_forecast.score_a = season_forecast.score_b)
    OR (season_fixture.team_b_id = '%(team_id)s' AND season_forecast.score_a = season_forecast.score_b)
    )    
    """ % ({'team_id':team_id})
    return executeRawSqlQuery(request)      

def count_team_forecasts_lose(team_id):
    request = """
    SELECT COUNT(*)
    FROM season_forecast, season_fixture
    WHERE season_forecast.fixture_id = season_fixture.id
    AND (
     (season_fixture.team_a_id = '%(team_id)s' AND season_forecast.score_a < season_forecast.score_b)
    OR (season_fixture.team_b_id = '%(team_id)s' AND season_forecast.score_a > season_forecast.score_b)
    )    
    """ % ({'team_id':team_id})
    return executeRawSqlQuery(request)
    
def league_table():
    """
    return the full league table for the entire season
    """
    request = """
    SELECT season_team.name AS team, sum(points) AS points, 
    count(season_table.week)-1 AS played, 
    sum(win) AS win, sum(draw) AS draw, sum(lose) AS lose, 
    sum(goal_for) AS goal_for, sum(goal_against) AS goal_against, 
    (sum(goal_for) - sum(goal_against)) AS diff
    FROM season_team, season_table
    WHERE season_team.id = season_table.team_id
    GROUP BY season_team.name
    ORDER BY points DESC, diff DESC, goal_for DESC, goal_against ASC,win DESC, draw DESC, lose DESC, played DESC, team ASC
    """
    return executeRawSqlQuery(request)

def league_table_with_teamid():
    """
    return the full league table for the entire season, with team id
    """
    request = """
    SELECT season_team.id AS team_id,season_team.name AS team_name, sum(points) AS points, 
    count(season_table.week)-1 AS played, 
    sum(win) AS win, sum(draw) AS draw, sum(lose) AS lose, 
    sum(goal_for) AS goal_for, sum(goal_against) AS goal_against, 
    (sum(goal_for) - sum(goal_against)) AS diff
    FROM season_team, season_table
    WHERE season_team.id = season_table.team_id
    GROUP BY season_team.id, season_team.name
    ORDER BY points DESC, diff DESC, goal_for DESC, goal_against ASC,win DESC, draw DESC, lose DESC, played DESC, team_name ASC
    """
    return executeRawSqlQuery(request)

def league_table_until(week):
    """
    returns the full league table until the given week
    """
    request = """
    SELECT season_team.name AS team, sum(points) AS points,
    count(season_table.week)-1 AS played, 
    sum(win) AS win, sum(draw) AS draw, sum(lose) AS lose, 
    sum(goal_for) AS goal_for, sum(goal_against) AS goal_against, 
    (sum(goal_for) - sum(goal_against)) AS diff
    FROM season_team, season_table
    WHERE season_team.id = season_table.team_id
    AND week <= %s
    GROUP BY season_team.name
    ORDER BY points DESC, diff DESC, goal_for DESC, goal_against ASC,win DESC, draw DESC, lose DESC, played DESC, team ASC
    """%week
    return executeRawSqlQuery(request)

def league_table_until_with_teamid(week):
    """
    return the full league table for the entire season, with team id
    """
    request = """
    SELECT season_team.id AS team_id,season_team.name AS team_name, sum(points) AS points, 
    count(season_table.week)-1 AS played, 
    sum(win) AS win, sum(draw) AS draw, sum(lose) AS lose, 
    sum(goal_for) AS goal_for, sum(goal_against) AS goal_against, 
    (sum(goal_for) - sum(goal_against)) AS diff
    FROM season_team, season_table
    WHERE season_team.id = season_table.team_id
    AND week <= %s
    GROUP BY season_team.id, season_team.name
    ORDER BY points DESC, diff DESC, goal_for DESC, goal_against ASC,win DESC, draw DESC, lose DESC, played DESC, team_name ASC
    """%week
    return executeRawSqlQuery(request)

def user_table_with_bonus():
    """
    returns the full players table with season forecast bonus
    """
    request = """
    SELECT c.id,
           c.name,
           c.points, 
           c.scores, 
           c.issues, 
           c.matches,
           c.points + IF (ISNULL(c.bonus),0,c.bonus) as total,
           c.bonus
    FROM(
        SELECT * from
            (SELECT season_player.id,
               season_player.name,
               sum(points) as points, 
               sum(score) as scores, 
               sum(issue) as issues, 
               count(points) as matches
            FROM season_forecast
            INNER JOIN season_player
            ON season_forecast.user_id = season_player.id
            GROUP BY season_player.id, season_player.name
            HAVING count(points) > 0
            ORDER BY points DESC, scores DESC, 
                 issues DESC, matches, season_player.name 
    
                 )a
    
                 LEFT OUTER JOIN (SELECT season_leagueforecast.user_id, season_leagueforecast.points as bonus
        FROM season_leagueforecast
        )b
        ON a.id = b.user_id
    )c
    ORDER BY ISNULL(total)ASC, total DESC, points DESC, scores DESC, 
             issues DESC, matches, name, id
    """
    #ISNULL(total) ASC, total -->MySql
    #total DESC NULLS LAST->PostGreSql
    return executeRawSqlQuery(request)
    
def weeks_goals(minmax):
    """
    returns either the list of weeks
    for either most or less goals scored
    @params minmax: min|max
    """
    request = """
    SELECT *
    FROM (
        SELECT week, sum( score_a ) + sum( score_b ) AS goals
        FROM season_fixture
        GROUP BY week
    )weeks_goals
    WHERE goals = (
        SELECT %s( goals )
        FROM (
            SELECT week, sum( score_a ) + sum( score_b ) AS goals
            FROM season_fixture
            GROUP BY week ) weeks_goals
        )
    """ % (minmax)
    return executeRawSqlQuery(request)
    
def weeks_most_goals():
    """
    returns the list of weeks with most goals scored
    """
    return weeks_goals('max')

def weeks_lest_goals():
    """
    returns the list of weeks with less goals scored
    """
    return weeks_goals('min')

def total_goals_scored():
    """
    returns the number of goals scored during the season 
    """
    request = """
    SELECT SUM(score_a) + SUM(score_b)
    FROM season_fixture
    WHERE score_a IS NOT NULL
    AND score_b IS NOT NULL
    """ 
    return executeRawSqlQuery(request)

def avg_goals_scored():
    """
    returns the average goals scored by match for the season
    NB: returns floating number in MYSQL, not POSTGRESQL
    """
    request = """
    SELECT (SUM(score_a) + SUM(score_b)) / COUNT(id)
    FROM season_fixture
    WHERE score_a IS NOT NULL
    AND score_b IS NOT NULL
    """ 
    return executeRawSqlQuery(request)

def goals_scored(minmax):
    """
    returns the number (most or less)
    of goals scored during one week 
    @params minmax: min|max
    """
    request = """
    SELECT %s( goals )
    FROM (
          SELECT sum( score_a ) + sum( score_b ) AS goals
          FROM season_fixture 
          GROUP BY week 
          ) weeks_goals
    """ % (minmax)
    return executeRawSqlQuery(request)

def most_goals_scored():
    """
    returns the highest number of goals scored during one week
    """
    return goals_scored('max')

def less_goals_scored():
    """
    returns the lowest number of goals scored during one week
    """
    return goals_scored('min')

def goals_scored_home(team_id):
    """
    returns the number of goals scored by a team at home
    """
    request = """
    SELECT SUM(score_a) 
    FROM season_fixture 
    WHERE team_a_id = '%s'
    """ % (team_id)
    return executeRawSqlQuery(request)

def goals_scored_away(team_id):
    """
    returns the number of goals scored by a team away
    """
    request = """
    SELECT SUM(score_b) 
    FROM season_fixture 
    WHERE team_b_id = '%s'
    """ % (team_id)
    return executeRawSqlQuery(request)

def goals_taken_home(team_id):
    """
    returns the number of goals taken by a team at home
    """
    request = """
    SELECT SUM(score_b) 
    FROM season_fixture 
    WHERE team_a_id = '%s'
    """ % (team_id)
    return executeRawSqlQuery(request)

def goals_taken_away(team_id):
    """
    returns the number of goals taken by a team away
    """
    request = """
    SELECT SUM(score_a) 
    FROM season_fixture 
    WHERE team_b_id = '%s'
    """ % (team_id)
    return executeRawSqlQuery(request)

def matches_played(team_id):
    """
    returns the number of matches played by a team
    """
    request = """
    SELECT COUNT(id) 
    FROM season_fixture 
    WHERE (team_a_id = '%(team_id)s'
    OR team_b_id = '%(team_id)s')
    AND (score_a IS NOT NULL
    AND score_b IS NOT NULL)
    """ % ({'team_id':team_id})
    return executeRawSqlQuery(request)

def team_points(team_id):
    """
    returns the number of points of a team
    """
    request = """
    SELECT SUM(points) 
    FROM season_table 
    WHERE team_id = '%s'
    """ % team_id
    return executeRawSqlQuery(request)
    