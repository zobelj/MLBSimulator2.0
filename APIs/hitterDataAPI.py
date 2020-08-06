import pandas as pd
import unidecode
import json

def loadData():
    data = pd.read_csv("data/mlb_2019_hitters.csv")

    names = list(data.loc[:, 'Name'])
    ops = list(data.loc[:, 'OPS+'].fillna(0))
    pa = list(data.loc[:, 'PA'].fillna(0))

    for i in range(len(names)):
        names[i] = names[i].split('\\')[0].replace('*', '').replace('#', '').replace(' Jr.', '').strip()
        names[i] = unidecode.unidecode(names[i])

    myDict = {names[i]: [pa[i], ops[i]] for i in range(len(names))}
    
    return(myDict)

def saveToJSON(data_dict):
    with open('data/hitters_2019.json', 'w') as outfile:
        json.dump(data_dict, outfile)

saveToJSON(loadData())


