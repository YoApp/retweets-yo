#!/usr/bin/python

#-----------------------------------------------------------------------
# yo-retweets
#  - Yo a tweet that gets more than X retweets 
#-----------------------------------------------------------------------

from twitter import *
import os
import urlparse
import redis
import requests

redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
redis = redis.Redis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password)

# these tokens are necessary for user authentication
# (created within the twitter developer API pages)
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

# create twitter API object
auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)
twitter = Twitter(auth = auth)

class Account:

	def __init__(self, twitter_handle, yo_api_token, threshold):
		self.twitter_handle = twitter_handle
		self.yo_api_token = yo_api_token
		self.threshold = threshold

# twitter accounts to track,  the Yo API token to Yo from, and the threshold of how many retweets
accounts = [
	Account(twitter_handle='TechCrunch', yo_api_token='', threshold=200)
]

for account in accounts:

	print 'running for ' + account.twitter_handle

	twitter_handle = account.twitter_handle

	# perform a basic search 
	# twitter API docs: https://dev.twitter.com/docs/api/1/get/search
	results = twitter.statuses.user_timeline(screen_name = twitter_handle)

	for tweet in results:
		if tweet['retweet_count'] > account.threshold:
			print 'found a tweet'
			tweet_url = 'http://twitter.com/' + twitter_handle + '/status/' + tweet['id_str']
			if redis.get(tweet_url):
				print 'already Yoed this url'
				continue  # already Yoed this url
			requests.post("http://api.justyo.co/yoall/", data={'api_token': account.yo_api_token, 'link': tweet_url})
			redis.set(tweet_url, 'sent')



