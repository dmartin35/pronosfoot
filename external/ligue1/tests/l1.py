import requests


r = requests.get("https://ma-api.ligue1.fr/championships-settings")


championship_id = None
championship_settings = {}


for id, settings in r.json().get("championships", []).items():
    if settings["shortBrand"] == "L1":
        championship_id = id
        championship_settings = settings

        break

    """
    firstGameWeekNumber	1
    lastGameWeekNumber	34
    gameWeeks	34
    clubsQuantity	18
    """

if not championship_id:
    raise Exception("championship id not found")


print("championship_id", championship_id)
# print("championship_settings", championship_settings)



#  full calendar - whout match details - 
# 
r = requests.get(f"https://ma-api.ligue1.fr/championship-calendar/{championship_id}")

games = r.json()

print(games['gameWeeks']['1'])

year = 2024



# get teams  - from first week games

r = requests.get(f"https://ma-api.ligue1.fr/championship-matches/championship/{championship_id}/game-week/1?season={year}")


matches = r.json().get('matches', [])

teams = []
teams.extend([m["home"]["clubIdentity"]["officialName"] for m in matches])
teams.extend([m["away"]["clubIdentity"]["officialName"] for m in matches])
teams = sorted(teams)
print(teams)



# get calendar 
for week in range(1, championship_settings["gameWeeks"]+1):
    r = requests.get(f"https://ma-api.ligue1.fr/championship-matches/championship/{championship_id}/game-week/{week}?season={year}")
    matches = r.json().get('matches', [])

    for match in matches:
        team_home = match["home"]["clubIdentity"]["officialName"]
        team_away = match["away"]["clubIdentity"]["officialName"]
        # team_away = match["away"]["clubIdentity"]["shortName"]
        match_date = match["date"]
        print(type(match_date), match_date)
        print(match_date, team_home, team_away)
    break
print("...")



# match details for a given week 
game_week = 1
r = requests.get(f"https://ma-api.ligue1.fr/championship-matches/championship/{championship_id}/game-week/{game_week}?season={year}")

        # match['period'] == "postMatch" ? 
        # match['isLive'] == False
        #score_home = match["home"].get("score")
        #score_away = match["away"].get("score")
