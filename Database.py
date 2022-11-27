from geopy.geocoders import Nominatim
import redis
import json

class Database:
    def __init__(self, api):
        self.api = api
        self.r = redis.Redis(host="localhost")

    def populate(self, hashtag):
        q = hashtag + " -filter:retweets -has:geo" if hashtag.startswith("#") else "#" + hashtag + " -filter:retweets -has:geo"
        print(q)
        tweets = self.api.search_tweets(q, count=20, tweet_mode='extended')
        for tweet in tweets:
            geolocator = Nominatim(user_agent="request")
            geo_location = geolocator.geocode(tweet.user.location)
            if geo_location != None:
                self.r.set(tweet.id, json.dumps([geo_location.latitude, geo_location.longitude, tweet.user.screen_name]))

    def expose_db(self):
        for key in self.r.scan_iter('*'):
            print(key)
            print(json.loads(self.r.get(key)))

    def flush(self):
        self.r.flushdb()