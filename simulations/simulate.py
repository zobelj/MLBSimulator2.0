import numpy as np

numRuns = 30

def simulateMatchup(away_RG, home_RG, hFA):

    if(hFA != 0):
        away_prob = simulateGame(away_RG, -1)
        home_prob = simulateGame(home_RG, 1)
    elif(hFA == 0):
        away_prob = simulateGame(away_RG, 0)
        home_prob = simulateGame(home_RG, 0)

    probMatrix = [[0 for i in range(len(away_prob))] for j in range(len(home_prob))]

    for i in range(0, len(away_prob)):
        for j in range(0, len(home_prob)):
            probMatrix[i][j] = away_prob[i] * home_prob[j]

    # calculate sum probability of either team winning
    team1Wins = []
    team2Wins = []
    ties = []

    for i in range(len(probMatrix)):
        for j in range(len(probMatrix)):
            if i<j:
                team1Wins.append(probMatrix[j][i])
            elif i>j:
                team2Wins.append(probMatrix[j][i])
            elif i==j:
                ties.append(probMatrix[i][j])

    tiesProb = sum(ties) * 100
    if(hFA == 0):
        team1WinProb = sum(team1Wins) * 100 + 0.5 * tiesProb
        team2WinProb = sum(team2Wins) * 100 + 0.5 * tiesProb
    else:
        team1WinProb = sum(team1Wins) * 100 + 0.53 * tiesProb
        team2WinProb = sum(team2Wins) * 100 + 0.47 * tiesProb

    extra = 100 - (team1WinProb + team2WinProb)

    ratio1 = team1WinProb / (team1WinProb + team2WinProb)
    ratio2 = team2WinProb / (team1WinProb + team2WinProb)

    team1WinProb += extra * ratio1
    team2WinProb += extra * ratio2

    return(team1WinProb, team2WinProb)

def simulateGame(team_RG, hFA):

    if(hFA == 1):
        team_RG += 0.075
    elif(hFA == -1):
        team_RG -= 0.075
    elif(hFA == 0):
        pass

    RI = team_RG / 9

    # initialize constants and helper variables
    c = 0.767
    variance = (team_RG**2/9) + (team_RG*2/c - team_RG)
    r = team_RG**2/(variance - team_RG)
    B = variance/team_RG - 1

    a = (1 + B)**(-r)
    z = (RI/(RI + c*RI**2))**9

    # calculate shutout probabilities for negative binomial and enby
    nbProb = [0] * numRuns
    nbProb[0] = a

    enbyGameProb = [0] * numRuns
    enbyGameProb[0] = z

    # calculate unmodified nb distribution for each run total
    for k in range(1, numRuns):
        
        rS = 1

        for j in range(k):
            rS *= r + j

        nbProb[k] = rS * B**k / (np.math.factorial(k) * ((1+B)**(r+k)))
    # modify nb distribution with tango distribution
    for h in range(1, numRuns):
        enbyGameProb[h] = (1 - z) * nbProb[h] / (1 - a)

    return(enbyGameProb)