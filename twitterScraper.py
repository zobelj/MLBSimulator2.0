import GetOldTweets3 as got
import re

username = 'DailyMLBLineup'
count = 100

tweetCriteria = got.manager.TweetCriteria().setUsername(username).setMaxTweets(count)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
user_tweets = [[tweet.date, tweet.text] for tweet in tweets]

positions = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH']

def getTeamLineup(tweet_data):
    # split up tweet data into text and info
    #tweet_date = str(tweet_data[0]).split(' ')[0]
    tweet_text = tweet_data[1]
    pitcher = tweet_text.split(' : ')[1]
    lineup = []

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

def getAllLineups(date):
    teams = []
    lineups = []

    for i in range(count):
        if(date in user_tweets[i][1]):
            team, lineup = getTeamLineup(user_tweets[i])
            teams.append(team)
            lineups.append(lineup)

    all_lineups_dict = {teams[i]:lineups[i] for i in range(len(teams))}

    return(all_lineups_dict)

all_lineups_dict = getAllLineups('08/02/20')

print(all_lineups_dict)
