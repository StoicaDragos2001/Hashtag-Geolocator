from threading import *
from APIauthenticator import APIauthenticator
from Database import Database
import tweepy as tweepy


if __name__ == '__main__':
    authenticator = APIauthenticator("config.ini")
    api = tweepy.API(authenticator.get_api_auth())

    db = Database(api)
    hashtag = input("Search for a twitter hashtag: ")
    daemon = Thread(target=db.populate(hashtag), daemon=True)
    daemon.start()
    db.populate(hashtag)
    num = input("Number of instances: ")
    db.expose_db()

    db.flush()
