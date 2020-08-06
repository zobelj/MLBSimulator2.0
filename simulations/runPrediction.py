import json
import unidecode
from bs4 import BeautifulSoup
import requests

name_to_abbrev = {'arizonadiamondbacks': 'ARI', 'atlantabraves': 'ATL', 'baltimoreorioles': 'BAL', 'bostonredsox': 'BOS', 'chicagowhitesox': 'CHW', 'chicagocubs': 'CHC', 'cincinnatireds': 'CIN', 'clevelandindians': 'CLE', 'coloradorockies': 'COL', 'detroittigers': 'DET', 'houstonastros': 'HOU', 'kansascityroyals': 'KCR','losangelesangels': 'LAA', 'losangelesdodgers': 'LAD','miamimarlins': 'MIA', 'milwaukeebrewers': 'MIL', 'minnesotatwins': 'MIN', 'newyorkyankees': 'NYY', 'newyorkmets': 'NYM','oaklandathletics': 'OAK', 'philadelphiaphillies': 'PHI', 'pittsburghpirates': 'PIT','sandiegopadres': 'SDP', 'sanfranciscogiants': 'SFG','seattlemariners': 'SEA', 'st.louiscardinals': 'STL', 'tampabayrays': 'TBR', 'texasrangers': 'TEX', 'torontobluejays': 'TOR', 'washingtonnationals': 'WSN'}

def getPredictedRG(team, lineup, oppTeam, oppPitcher):
    rg_data = json.load(open('data/mlb_2019_teams.json'))
    pitcher_data = json.load(open('data/mlb_2019_pitchers.json'))

    team_RG = rg_data[team][0]
    team_OPS = rg_data[team][1]
    try:
        x = pitcher_data[oppPitcher]
    except:
        x = [4.57, 4.57, 5.3, 1]
        print("Unable to find data for {}. Using league average instead.".format(oppPitcher))

    oppPitcher_innings = float(int(x[2]) + ((x[2] - int(x[2])) * 3.33)) / x[3]
    oppPitcher_RA = ((x[0] + x[1]) / 2) * oppPitcher_innings / 9

    bullpen_RA = (rg_data[oppTeam][3] / 9) * (9 - oppPitcher_innings)
    predicted_RA = oppPitcher_RA + bullpen_RA
    
    lineup_OPS = getLineupOPS(lineup, team)
    ops_multiplier = lineup_OPS / team_OPS

    predicted_RS = team_RG * ops_multiplier

    predicted_RG = (predicted_RS + predicted_RA) / 2

    return(predicted_RG)

def getPredictedRG_Basic(team, opponent):
    rg_data = json.load(open('data/mlb_2019_teams.json'))

    team_RG = rg_data[team][0]
    opp_RA = rg_data[opponent][2]

    predicted_RG = (team_RG + opp_RA) / 2

    return(predicted_RG)

def getLineupOPS(lineup, team_name):
    hitters_2019 = json.load(open('data/hitters_2019.json'))
    hitters_2020 = get2020Data(team_name, lineup)

    for i in range(len(lineup)):
        lineup[i] = lineup[i].strip()

    ops_2019 = []
    pa_2019 = []
    wOPS_2019 = 0

    ops_2020 = []
    pa_2020 = []
    wOPS_2020 = 0

    for name in lineup:
        try:
            ops_2019.append(hitters_2019[name.strip()][1])
        except:
            ops_2019.append(0)
        try:
            ops_2020.append(hitters_2020[name.strip()][1])
        except:
            ops_2020.append(0)

        try:
            pa_2019.append(hitters_2019[name.strip()][0])
        except:
            pa_2019.append(0)
        try:
            pa_2020.append(hitters_2020[name.strip()][0])
        except:
            pa_2020.append(0)

    wOPS_2019 = int(sum([ops_2019[i] * pa_2019[i] for i in range(len(ops_2019))]) / sum(pa_2019))
    wOPS_2020 = int(sum([ops_2020[i] * pa_2020[i] for i in range(len(ops_2020))]) / sum(pa_2020))

    wOPS = (wOPS_2019 + wOPS_2020) / 2

    return(wOPS)

def get2020Data(team_name, player_names):
    #abbrev = name_to_abbrev[team_name.lower().replace(' ', '')]

    url = 'https://www.baseball-reference.com/teams/{}/2020.shtml' .format(team_name.upper())

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    names_2020 = soup('td', {'data-stat' : 'player'})[:15]
    pa_2020 = soup('td', {'data-stat' : 'PA'})[:15]
    ops_2020 = soup('td', {'data-stat' : 'onbase_plus_slugging_plus'})[:15]

    for i in range(len(names_2020)):
        names_2020[i] = names_2020[i].get_text().replace('#', '').replace('*', '').replace('10-day IL', '').replace('45-day IL', '').replace('Jr.', '')
        try:
            ops_2020[i] = int(ops_2020[i].get_text())
        except:
            ops_2020[i] = 0
        try:
            pa_2020[i] = int(pa_2020[i].get_text())
        except:
            pa_2020[i] = 0
        names_2020[i] = unidecode.unidecode(names_2020[i]).strip()

    data_2020 = {names_2020[i]: [pa_2020[i], ops_2020[i]] for i in range(len(names_2020))}

    return(data_2020)

#getPredictedRG('CHW', 'WSN', 'Max Scherzer')