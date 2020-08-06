import requests
from bs4 import BeautifulSoup
import unidecode

name_to_abbrev = {'arizonadiamondbacks': 'ARI', 'atlantabraves': 'ATL', 'baltimoreorioles': 'BAL', 'bostonredsox': 'BOS', 'chicagowhitesox': 'CHW', 'chicagocubs': 'CHC', 'cincinnatireds': 'CIN', 'clevelandindians': 'CLE', 'coloradorockies': 'COL', 'detroittigers': 'DET', 'houstonastros': 'HOU', 'kansascityroyals': 'KCR','losangelesangels': 'LAA', 'losangelesdodgers': 'LAD','miamimarlins': 'MIA', 'milwaukeebrewers': 'MIL', 'minnesotatwins': 'MIN', 'newyorkyankees': 'NYY', 'newyorkmets': 'NYM','oaklandathletics': 'OAK', 'philadelphiaphillies': 'PHI', 'pittsburghpirates': 'PIT','sandiegopadres': 'SDP', 'sanfranciscogiants': 'SFG','seattlemariners': 'SEA', 'st.louiscardinals': 'STL', 'tampabayrays': 'TBR', 'texasrangers': 'TEX', 'torontobluejays': 'TOR', 'washingtonnationals': 'WSN'}

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

