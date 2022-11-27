import configparser
import tweepy


class APIauthenticator:
    def __init__(self, conf_location):
        self.conf_location = conf_location
        self.assume_credentials()

    def assume_credentials(self):
        conf = configparser.ConfigParser()
        conf.read(self.conf_location)
        self.api_key = conf["twitter"]["api_key"]
        self.api_key_secret = conf["twitter"]["api_key_secret"]

        self.access_token = conf["twitter"]["access_token"]
        self.access_token_secret = conf["twitter"]["access_token_secret"]

    def get_api_auth(self):
        authentication = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        authentication.set_access_token(self.access_token, self.access_token_secret)
        return authentication