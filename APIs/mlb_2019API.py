import pandas as pd
import unidecode
import json
import numpy as np

def loadHitterData():
    data = pd.read_csv("data/mlb_2019_hitters.csv")

    names = list(data.loc[:, 'Name'])
    ops = list(data.loc[:, 'OPS+'].fillna(0))
    pa = list(data.loc[:, 'PA'].fillna(0))

    for i in range(len(names)):
        names[i] = names[i].split('\\')[0].replace('*', '').replace('#', '').replace(' Jr.', '').strip()
        names[i] = unidecode.unidecode(names[i])

    myDict = {names[i]: [pa[i], ops[i]] for i in range(len(names))}
    
    return(myDict)

def loadPitcherData():
    data = pd.read_csv("data/mlb_2019_pitchers.csv")

    names = list(data.loc[:, 'Name'])
    era = list(data.loc[:, 'ERA'].fillna(0).replace([np.inf, -np.inf], 100))
    fip = list(data.loc[:, 'FIP'].fillna(0).replace([np.inf, -np.inf], 100))
    innings = list(data.loc[:, 'IP'].fillna(0))
    starts = list(data.loc[:, 'GS'].fillna(0))

    for i in range(len(names)):
        names[i] = names[i].split('\\')[0].replace('*', '').replace('#', '').replace(' Jr.', '').strip()
        names[i] = unidecode.unidecode(names[i])

    myDict = {names[i]: [era[i], fip[i], innings[i], starts[i]] for i in range(len(names))}

    return(myDict)

def loadTeamData():
    data_offense = pd.read_csv("data/mlb_2019_teams_offense.csv")
    data_defense = pd.read_csv("data/mlb_2019_teams_defense.csv")

    teams = list(data_offense.loc[:, 'Tm'])
    runs_per_game = list(data_offense.loc[:, 'R/G'].fillna(0))
    team_ops = list(data_offense.loc[:, 'OPS+'].fillna(0))
    runs_allowed = list(data_defense.loc[:, 'RA/G'].fillna(0))
    bullpen_ERA = list(data_defense.loc[:, 'bERA'].fillna(0))

    myDict = {teams[i]: [runs_per_game[i], team_ops[i], runs_allowed[i], bullpen_ERA[i]] for i in range(len(teams))}
    
    return(myDict)

def saveToJSON(data_dict, name):
    with open('data/{}'.format(name), 'w') as outfile:
        json.dump(data_dict, outfile)

#saveToJSON(loadHitterData(), 'mlb_2019_hitters.json')
#saveToJSON(loadPitcherData(), 'mlb_2019_pitchers.json')
saveToJSON(loadTeamData(), 'mlb_2019_teams.json')


