from bs4 import BeautifulSoup
import requests
import json

def getMatchups(date):
    url = 'https://www.mlb.com/scores/{}'.format(date)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    teams = soup(class_="sc-pbIaG fCAMpt")

    for i in range(len(teams)):
        teams[i] = teams[i].get_text().lower()

    matchupsH2A = dict(zip(teams[1::2], teams[::2]))

    matchupsA2H = dict(zip(teams[::2], teams[1::2]))

    matchups = {'home': matchupsH2A, 'away': matchupsA2H}
    return(matchups)

def saveToJSON(matchups):
    with open("data/matchups.json", "w") as outfile:
        json.dump(matchups, outfile)

def updateMatchupsJSON(date):
    saveToJSON(getMatchups(date))
    