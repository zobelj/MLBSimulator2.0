import pandas as pd
import json
import numpy as np

name_to_abbrev = {'arizonadiamondbacks': 'ARI', 'atlantabraves': 'ATL', 'baltimoreorioles': 'BAL', 'bostonredsox': 'BOS', 'chicagowhitesox': 'CHW', 'chicagocubs': 'CHC', 'cincinnatireds': 'CIN', 'clevelandindians': 'CLE', 'coloradorockies': 'COL', 'detroittigers': 'DET', 'houstonastros': 'HOU', 'kansascityroyals': 'KCR','losangelesangels': 'LAA', 'losangelesdodgers': 'LAD','miamimarlins': 'MIA', 'milwaukeebrewers': 'MIL', 'minnesotatwins': 'MIN', 'newyorkyankees': 'NYY', 'newyorkmets': 'NYM','oaklandathletics': 'OAK', 'philadelphiaphillies': 'PHI', 'pittsburghpirates': 'PIT','sandiegopadres': 'SDP', 'sanfranciscogiants': 'SFG','seattlemariners': 'SEA', 'st.louiscardinals': 'STL', 'tampabayrays': 'TBR', 'texasrangers': 'TEX', 'torontobluejays': 'TOR', 'washingtonnationals': 'WSN'}


def getESPN(type):
    dfs = pd.read_html('https://www.espn.com/mlb/stats/team/_/view/{}'.format(type))

    data = dfs[0]
    stats = dfs[1]

    teams = list(data['Team'])
    for i in range(len(teams)):
        teams[i] = name_to_abbrev[teams[i].lower().replace(' ', '')]
    stat_names = stats.columns

    data_dict = {teams[j]: {stat_names[i]: stats.iloc[j, :][i] for i in range(len(stat_names))} for j in range(len(teams))}

    return(data_dict)

def combinedDicts():
    off_dict = getESPN('batting')
    pitch_dict = getESPN('pitching')
    all_dict = {'batting': off_dict, 'pitching': pitch_dict}

    return(all_dict)

def saveToJSON(data_dict, name):
    with open('data/{}'.format(name), 'w') as outfile:
        json.dump(data_dict, outfile)

def update2020Data():
    saveToJSON(combinedDicts(), 'mlb_2020_all.json')
