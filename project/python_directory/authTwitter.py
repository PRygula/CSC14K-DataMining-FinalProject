# Chris DeMarco and Patrick Rygula
# Sept 12, 2016
# Mining Social Web - Twitter Auth
# Tokens are taken out for security reasons.

import twitter

def authTW():
	CONSUMER_KEY = ''
	CONSUMER_SECRET = ''

	OAUTH_TOKEN = ''
	OAUTH_TOKEN_SECRET = ''

	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
	twitter_api = twitter.Twitter(auth = auth)

	return twitter_api

def authTWStream():
	CONSUMER_KEY = ''
	CONSUMER_SECRET = ''

	OAUTH_TOKEN = ''
	OAUTH_TOKEN_SECRET = ''

	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
	twitter_stream_api = twitter.TwitterStream(auth = auth)

	return twitter_stream_api
