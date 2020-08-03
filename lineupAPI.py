import GetOldTweets3 as got
import re
import datetime
import json

# global variable declarations
username = 'DailyMLBLineup' # twitter account username
positions = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH']

# download recent tweets
def getTweets(date):
    global user_tweets

    month, day, year = date.split('/')
    year = '20' + year
    base_date_str = year + ' ' + month + ' ' + day
    base_date_obj = datetime.datetime.strptime(base_date_str, '%Y %m %d')
    since_date = str((base_date_obj - datetime.timedelta(days=1)).date())
    until_date = str((base_date_obj + datetime.timedelta(days=1)).date())

    print(since_date)
    print(until_date)
    tweetCriteria = got.manager.TweetCriteria().setUsername(username).setSince(since_date).setUntil(until_date)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    user_tweets = [[tweet.date, tweet.text] for tweet in tweets]

# extract team, lineup, and pitcher from a given tweet
def getTeamLineup(tweet_data):
    tweet_text = tweet_data[1]
    pitcher = tweet_text.split(' : ')[1]
    lineup = []

    # get team name
    team = re.search('#(.+?) Lineup', tweet_text).group(1)

    # extract hitters 1 through 8
    for i in range(8):
        player = re.search(rf'{i+1}\. (.+?) {i+2}\.', tweet_text).group(1)
        lineup.append(player)

    # add 9 hitter
    lineup.append(re.search(r'9\. (.+?) Start', tweet_text).group(1))

    # remove positions from string
    for i in range(9):
        for pos in positions:
            lineup[i] = lineup[i].replace(pos, '').strip()
            if lineup[i][-2:] == ' C' or lineup[i][-2:] == ' P':
                lineup[i] = lineup[i][:-2]
         
    lineup.append(pitcher)

    return([team, lineup])

# save all lineups from a given date into a dictionary {team_name:lineup}
def getAllLineups(date):
    teams = []
    lineups = []

    for i in range(len(user_tweets)):
        if(date in user_tweets[i][1]):
            team, lineup = getTeamLineup(user_tweets[i])
            teams.append(team)
            lineups.append(lineup)

    all_lineups_dict = {teams[i]:lineups[i] for i in range(len(teams))}

    return(all_lineups_dict)

def saveToJSON(myDict):
    with open("data/lineups.json", "w") as outfile:
        json.dump(myDict, outfile)

# download tweets and extract all found lineups
def updateLineupsJSON(date):

    getTweets(date)
    all_lineups_dict = getAllLineups(date)
    saveToJSON(all_lineups_dict)
