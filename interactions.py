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
    
    def __init__(self, twitter_api, twit, sqldb, bot_name):
        self.api = twitter_api
        self.twitter = twit
        self.db = sqldb
        self.bot_name = bot_name
        
    def log(self, msg):
        print "LOG (INTERACTION): " + msg
        
    def process_quote(self, tweet):
        self.log("Checking for quotes...")
        parsed = re.split(' ', tweet.text)
        
        # if the tweet contains quote @user
        for i in range(len(parsed) - 1):
            word = parsed[i]
            if word == "quote":
                # get a random quote
                quote = self.db.get_quote(parsed[i+1])
                if quote:
                    self.api.tweet_reply(quote[6] + ": " + quote[3] \
                        + " (@" + tweet.user.screen_name + ")", tweet.id)
                    return quote
                else:
                    self.log("No quotes found.")
                    return None
        
        if (self.bot_name + " remember th") in tweet.text:
            quote_tweet = self.twitter.get_status(tweet.in_reply_to_status_id)
            quotee = quote_tweet.user.screen_name
            quote  = quote_tweet.text
            self.db.add_factoid("quote", "quote @" + quotee, quote, "remember", 0, "@" + quotee)
            self.api.tweet_reply("Ok @" + tweet.user.screen_name + "!" \
                + " (@" + quotee + ")", tweet.id)
            return quote
            
        elif not len(parsed) < 4:
            # specific quote retrival
            # syntax is @bot quote @user [keywords]
            if (parsed[0] == self.bot_name and parsed[1] == "quote"):
              quote = self.db.get_quote(parsed[2], re.split("@[^\s]+ ", tweet.text)[2])
              if quote:
                  self.api.tweet_reply(quote[6] + ": " + quote[3], tweet.id)
                  return quote
              else:
                  self.log("No quotes found.")
                  return None

            #otherwise ignore
            else:
                self.log("Ignored invalid quote operation: " + tweet.text)
                return None

        # random quote retrival
        elif len(parsed) == 3:
            if (parsed[0] == self.bot_name and parsed[1] == "quote"):
                quote = self.db.get_quote(parsed[2])
                if quote:
                    self.api.tweet_reply(quote[6] + ": " + quote[3] \
                        + " (@" + tweet.user.screen_name + ")", tweet.id)
                    return quote
                else:
                    self.log("No quotes found!")
                    return None
    

        # otherwise ignore
        else:
            self.log("Ignored invalid quote operation: " + tweet.text)
            return None

    # look for triggers in database
    def triggers(self, tweet):
        self.log("Checking for possible triggers...")
        factoid = self.db.get_factoid(tweet.text.replace(self.bot_name, ""))
        if factoid:
            # Append advice # if necessary
            if factoid[1] == "advice":
                self.api.tweet_reply("@" + tweet.user.screen_name + " " \
                    + "Advice #" + str(randint(1,999)) + ": " + factoid[3], tweet.id)
            else:
                self.api.tweet_reply("@" + tweet.user.screen_name + " " + factoid[3], tweet.id)
            return factoid
        else: 
            self.log("No triggers found.")
            return None
    
    def add_fact(self, tweet):
        parsed = tweet.text.split(' ')
        
        if parsed[0] == self.bot_name:
            parsed = parsed[1:] # strip out @bot_name
            
            # check if it is a cuddle request
            # TODO move this into a method
            if len(parsed) == 2 and parsed[0] == "cuddle":
                if parsed[1][0] == "@":
                    self.api.tweet_reply("@" + tweet.user.screen_name \
                        + " *cuddles* " + parsed[1], tweet.id)
            else:            
                pre  = ""
                post = ""
                get_pre_mode = True # check that we're getting the left side
                for word in parsed:
                    if word == "is":
                        get_pre_mode = False
                    elif get_pre_mode:
                        pre = pre + word + " "
                    else:
                        post = post + word + " "
                    
                # check that the fact is valid
                if (len(pre)>0 and len(post)>0):            
                    # remove trailing space
                    pre  = pre[:len(pre)-1]
                    post = post[:len(post)-1]
            
                    self.db.add_factoid("fact", pre, post, "is", 0, "@" + tweet.user.screen_name)
    
    def provide_help(self, tweet):
        if tweet.text == (self.bot_name + " --help"):
            self.api.tweet_reply("@" + tweet.user.screen_name + " My documentation is here: https://t.co/xmPavDZWxY", tweet.id)
                