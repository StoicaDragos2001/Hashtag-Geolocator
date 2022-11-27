from geopy.geocoders import Nominatim
import redis
import json


class Database:
    def __init__(self, api):
        self.api = api
        self.r = redis.Redis(host="localhost")

    def populate(self, hashtag):
        q = hashtag + " -filter:retweets -has:geo" if hashtag.startswith(
            "#") else "#" + hashtag + " -filter:retweets -has:geo"
        tweets = self.api.search_tweets(q, count=20, tweet_mode='extended')
        for tweet in tweets:
            geolocator = Nominatim(user_agent="request")
            geo_location = geolocator.geocode(tweet.user.location)
            if geo_location is not None:
                self.r.rpush("db", json.dumps(
                    {tweet.id: {"latitude": geo_location.latitude, "longitude": geo_location.longitude,
                                "screen_name": tweet.user.screen_name, "date": tweet.created_at}}, default=str))

    def expose_db(self):
        for i in self.r.lrange("db", 0, -1):
            print(i)

    def flush(self):
        self.r.flushdb()
