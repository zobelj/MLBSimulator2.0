import pandas as pd
import numpy as np

def historicalData():

    data_set = pd.read_csv("data/mlb_historical_data.csv")

    runs_game = list(data_set.loc[:, 'R/G'])

    corr_dict = {}


    for i in range(1, len(data_set.loc[0, :])):
        x_values = list(data_set.iloc[:, i])

        correlation_matrix = np.corrcoef(x_values, runs_game)
        correlation_xy = correlation_matrix[0,1]
        r_squared = correlation_xy**2

        corr_dict.update({i: r_squared})

    sorted_dict = sorted(corr_dict.items(), key=lambda x: x[1], reverse=True)

    print(sorted_dict)

def advancedData():
    data_set = pd.read_csv("data/mlb_historical_advanced.csv")

    runs_game = list(data_set.loc[:, 'R/G'])

    corr_dict = {}

    for i in range(1, len(data_set.loc[0, :])):
        x_values = list(data_set.iloc[:, i])

        correlation_matrix = np.corrcoef(x_values, runs_game)
        correlation_xy = correlation_matrix[0,1]
        r_squared = correlation_xy**2

        corr_dict.update({i: r_squared})

    sorted_dict = sorted(corr_dict.items(), key=lambda x: x[1], reverse=True)

    print(sorted_dict)

advancedData()
