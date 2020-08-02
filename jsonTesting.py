import json

# load json file into memory
f = open('odds.json')
data_json = json.load(f)


# variable declarations
matchups_lists = [] # list of pairs of teams playing eachother
home_teams = [] # list of each home team

matchup_odds = {} # dictionary of teams:odds

odds_lists = [0] # lists of odds, each games' split up into its own list
all_odds = [] # list of all odds for all games
sites_count = [] # number of sites offered for each game


# get a list of all home teams
for i in data_json['data']:
    matchups_lists.append(i['teams'])
    home_teams.append(i['home_team'])

# make sure every pair of teams is ordered away team, home team
'''
for i in range(len(home_teams)):
    if matchups_lists[i][0] == home_teams[i]:
        matchups_lists[i][0], matchups_lists[i][1] = matchups_lists[i][1], matchups_lists[i][0]
'''

# convert list of lists to list of tuples
matchups = tuple(map(tuple, matchups_lists))

# get all odds into one list of lists
for i in range(len(data_json['data'])):
    for j in data_json['data'][i]['sites']:
        all_odds.append(j['odds']['h2h'])

# get the number of sites offered for each matchup
for i in data_json['data']:
    sites_count.append(i['sites_count'])

# break up long list of odds into many lists by game
count = 0
odds_lists[0] = all_odds[0:sites_count[0]]
for i in range(len(home_teams)):
    count += sites_count[i]
    temp_odds_list = all_odds[count:count + sites_count[i]]

    odds_lists.append(temp_odds_list)
# delete empty element at the end of odds_lists
del odds_lists[-1]

# create dictionary of teams:odds
matchup_odds = {matchups[i]: odds_lists[i] for i in range(len(matchups))}

#print matchup for game 6 and its available odds
print(matchups[6])
print(matchup_odds[matchups[6]])
