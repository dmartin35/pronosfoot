from external.odds.fdj.api import get_odds

if __name__ == "__main__":
    for match, odds in get_odds().items():
        print(match, odds)