import tweepy

consumer_key        = ''
consumer_secret     = ''
access_token_key    = ''
access_token_secret = ''

class TwitterApi:
    api = None

    def log(self, msg):
        print "LOG (API): " + msg

    def connect(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        self.api = tweepy.API(auth)
        return self.api

    def tweet_reply(self, status, in_reply_to_status_id):
        log("Replying to " + in_reply_to_status_id +  "with: " + status)
        self.api.update_status(status, in_reply_to_status_id)
        
    def tweet_status(self, status):
        log("Tweeting: " + status)
        self.api.update_status(status)