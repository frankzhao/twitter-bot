# Frank Zhao 2014
# <frank@frankzhao.net>
# Interactions

import tweepy
import re
import database
import twitterapi
import interactions
from random import randint

class Interactions:
    
    bot_name = ""
    
    def __init__(self, twitter_api, sqldb, bot_name):
        self.api = twitter_api
        self.db = sqldb
        self.bot_name = bot_name
        
    def log(self, msg):
        print "LOG (INTERACTION): " + msg
        
    def process_quote(self, tweet):
            parsed = re.split(' ', tweet.text)
            
            # if the tweet contains quote @user
            for i in range(len(parsed) - 1):
                word = parsed[i]
                if word == "quote":
                    # get a random quote
                    quote = self.db.get_quote(parsed[i+1])
                    if quote != None:
                        self.api.tweet_reply("@" + quote[6] + ": " + quote[3] \
                            + " (@" + tweet.user.screen_name + ")", tweet.id)
                    return
            
            if (self.bot_name + " remember th") in tweet.text:
                quote_tweet = twitter.get_status(tweet.in_reply_to_status_id)
                quotee = quote_tweet.user.screen_name
                quote  = quote_tweet.text
                self.db.add_factoid("quote", "quote " + quotee, quote, "remember", 0, quotee)
                self.api.tweet_reply("Ok @" + tweet.user.screen_name + "!" \
                    + " (@" + quotee + ")", tweet.id)
            elif not len(parsed) < 4:
                # specific quote retrival
                # syntax is @bot quote @user [keywords]
                if (parsed[0] == self.bot_name and parsed[1] == "quote"):
                  quote = self.db.get_quote(parsed[2], re.split("@[^\s]+ ", tweet.text)[2])
                  if quote != None:
                      self.api.tweet_reply(quote[6] + ": " + quote[3], tweet.id)
    
                #otherwise ignore
                else: self.log("Ignored invalid quote operation: " + tweet.text)

            # random quote retrival
            elif len(parsed) == 3:
                if (parsed[0] == self.bot_name and parsed[1] == "quote"):
                    quote = self.db.get_quote(parsed[2])
                    if quote != None:
                        self.api.tweet_reply("@" + quote[6] + ": " + quote[3] \
                            + " (@" + twee.user.screen_name + ")", tweet.id)
        
    
            # otherwise ignore
            else: self.log("Ignored invalid quote operation: " + tweet.text)

    # look for triggers in database
    def triggers(self, tweet):
        self.log("Checking for possible triggers...")
        parsed = re.split(' ', tweet.text)
        for word in parsed:
            factoid = self.db.get_factoid(word)
            if factoid != None:
                # Append advice # if necessary
                if factoid[1] == "advice":
                    self.api.tweet_reply("@" + tweet.user.screen_name + " " \
                        + "Advice #" + str(randint(1,999)) + ": " + factoid[3], tweet.id)
                else:
                    self.api.tweet_reply("@" + tweet.user.screen_name + " " + factoid[3], tweet.id)
            else: self.log("No triggers found.")