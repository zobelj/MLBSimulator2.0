import GetOldTweets3 as got

username = 'DailyMLBLineup'
count = 5

tweetCriteria = got.manager.TweetCriteria().setUsername(username).setMaxTweets(count)

tweets = got.manager.TweetManager.getTweets(tweetCriteria)

user_tweets = [[tweet.date, tweet.text] for tweet in tweets]

print(user_tweets[3][1].splitlines())

