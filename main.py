from threading import *
from PyQt5.QtWidgets import QApplication
from APIauthenticator import APIauthenticator
from Database import Database
from Geolocator import Geolocator
from queue import Queue
from Utility import Utility
import tweepy as tweepy
import sys

if __name__ == '__main__':
    authenticator = APIauthenticator("config.ini")
    api = tweepy.API(authenticator.get_api_auth())
    num_input_res = Queue()

    db = Database(api)
    db.flush()
    hashtag = input("Search for a twitter hashtag: ")

    daemon = Thread(target=db.populate, daemon=True, args=([hashtag]))
    daemon.start()

    input_thread = Thread(target=Utility.get_num_input, args=([num_input_res]))
    input_thread.start()

    input_thread.join()
    daemon.join()

    print(f"Twitter hashtag: {hashtag}")
    num_input = num_input_res.get()
    print(f"Number of instances given: {num_input}")
    db.expose_db()

    app = QApplication(sys.argv)
    geolocator = Geolocator()
    geolocator.add_data(db.get_last_entries(num_input))
    geolocator.show()
    db.flush()
    sys.exit(app.exec_())
