import GetOldTweets3 as got
import re

username = 'DailyMLBLineup'
count = 5

tweetCriteria = got.manager.TweetCriteria().setUsername(username).setMaxTweets(count)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
user_tweets = [[tweet.date, tweet.text] for tweet in tweets]

leadoff = re.search(' 1. (.+?) 2.', user_tweets[2][1]).group(1)

positions = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']

for i in positions:
    leadoff = leadoff.replace(i, '').strip()

print(leadoff)