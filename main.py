from threading import *
from APIauthenticator import APIauthenticator
from Database import Database
from queue import Queue
from Utility import Utility
import tweepy as tweepy


# def get_num_input():
#     data = input("Number of instances: ")
#     num_input_res.put(data)


if __name__ == '__main__':
    authenticator = APIauthenticator("config.ini")
    api = tweepy.API(authenticator.get_api_auth())
    num_input_res = Queue()

    db = Database(api)
    hashtag = input("Search for a twitter hashtag: ")

    daemon = Thread(target=db.populate, daemon=True, args=([hashtag]))
    daemon.start()

    input_thread = Thread(target=Utility.get_num_input, args=([num_input_res]))
    input_thread.start()

    input_thread.join()
    daemon.join()

    print(f"Twitter hashtag: {hashtag}")
    print(f"Number of instances given: {num_input_res.get()}")
    db.expose_db()

    db.flush()
