from threading import *
from APIauthenticator import APIauthenticator
import redis
import tweepy as tweepy


if __name__ == '__main__':
    authenticator = APIauthenticator("config.ini")
    api = tweepy.API(authenticator.get_api_auth())

    tweets = api.search_tweets(q="#dev -filter:retweets -has:geo", count=5, tweet_mode='extended')

    for tweet in tweets:
        print(tweet.user.screen_name)
        print(tweet.id)
        print(tweet.full_text)
        print(tweet.user.location)
        print("-----------------------")

    hashtag = input("Search for a twitter hashtag:")
    num = input("Number of instances:")
