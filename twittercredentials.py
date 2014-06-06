import tweepy

consumer_key        = ''
consumer_secret     = ''
access_token_key    = ''
access_token_secret = ''

def connect():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)
    return api