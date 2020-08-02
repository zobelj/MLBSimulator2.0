import json

f = open('odds.json')

odds_json = json.load(f)

matchups = []
home_teams = []


for i in odds_json['data']:
    matchups.append(i['teams'])
    home_teams.append(i['home_team'])

for i in range(len(home_teams)):
    if matchups[i][0] == home_teams[i]:
        matchups[i][0], matchups[i][1] = matchups[i][1], matchups[i][0]

matchup_odds = [[0]] * len(home_teams)


for i in range(len(odds_json['data'])):
    for j in odds_json['data'][i]['sites']:
        matchup_odds[i].append(j['odds']['h2h'])

print(matchups)

