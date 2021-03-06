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

    # return all mentions as a string
    def tweet_mentions(self, tweet):
        parsed = re.split(' ', tweet.text)
        users = []
        for word in parsed:
            if word[0] == "@" and word != self.bot_name:
                users.append(word)

        new_status_mentions = ""
        for user in users:
            new_status_mentions = new_status_mentions + user + " "

        return new_status_mentions

    def process_quote(self, tweet):
        self.log("Checking for quotes...")
        parsed = re.split(' ', tweet.text)

        # if the tweet contains quote @user
        for i in range(len(parsed) - 1):
            word = parsed[i]
            word = word.lower()
            if word == "quote":
                # get a random quote
                quote = self.db.get_quote(parsed[i+1])
                if quote:
                    self.api.tweet_reply(quote[6] + ": " + quote[3] \
                        + " (@" + tweet.user.screen_name + ")", tweet.id)
                    return True
                else:
                    #self.log("No quotes found.")
                    user_tweets = self.api.user_timeline(parsed[i+1])
                    quote = user_tweets[randint(0,19)].text
                    if quote:
                        self.api.tweet_reply(parsed[i+1] + ": " + quote + " (@" + tweet.user.screen_name + ")", tweet.id)
                    else:
                        return False
                    return True

        if (self.bot_name + " remember th") in tweet.text.lower():
            quote_tweet = self.twitter.get_status(tweet.in_reply_to_status_id)
            quotee = quote_tweet.user.screen_name
            quote  = quote_tweet.text
            self.db.add_factoid("quote", "quote @" + quotee, quote, "remember", 0, "@" + quotee)
            self.api.tweet_reply("Ok @" + tweet.user.screen_name + "!" \
                + " (@" + quotee + ")", tweet.id)
            return True

        elif not len(parsed) < 4:
            # specific quote retrival
            # syntax is @bot quote @user [keywords]
            parsed[1] == parsed[1].lower()
            if (parsed[0] == self.bot_name and parsed[1] == "quote"):
              quote = self.db.get_quote(parsed[2], re.split("@[^\s]+ ", tweet.text)[2])
              if quote:
                  self.api.tweet_reply(quote[6] + ": " + quote[3], tweet.id)
                  return True
              else:
                  self.log("No quotes found.")
                  return False

            #otherwise ignore
            else:
                self.log("Ignored invalid quote operation: " + tweet.text)
                return False

        # random quote retrival
        elif len(parsed) == 3:
            if (parsed[0] == self.bot_name and parsed[1] == "quote"):
                quote = self.db.get_quote(parsed[2])
                if quote:
                    self.api.tweet_reply(quote[6] + ": " + quote[3] \
                        + " (@" + tweet.user.screen_name + ")", tweet.id)
                    return True
                else:
                    self.log("No quotes found!")
                    return False


        # otherwise ignore
        else:
            self.log("Ignored invalid quote operation: " + tweet.text)
            return False

    # look for triggers in database
    def triggers(self, tweet):
        self.log("Checking for possible triggers...")
        factoid = self.db.get_factoid(tweet.text.replace(self.bot_name, ""))
        if factoid:
            # Append advice # if necessary
            if factoid[1] == "advice":
                self.api.tweet_reply(self.tweet_mentions(tweet) + "@" + tweet.user.screen_name + " " \
                    + "Advice #" + str(randint(1,999)) + ": " + factoid[3], tweet.id)
            else:
                # check if it is a retweet
                try:
                    original_status = tweet.retweeted_status
                    orignal_user = original_status.user.screen_name

                    if factoid[1] == "fact":
                        self.api.tweet_reply(self.tweet_mentions(tweet) \
                            + "@" + original_user + " " + factoid[3] + " " \
                            + factoid[4] + " " + factoid[3], original_status.id)
                    else:
                        self.api.tweet_reply(self.tweet_mentions(tweet) \
                            + "@" + original_user + " " + factoid[3], original_status.id)
                # if not a retweet
                except:
                    if factoid[1] == "fact":
                        self.api.tweet_reply(self.tweet_mentions(tweet) \
                            + "@" + original_user + " " + factoid[3] + " " \
                            + factoid[4] + " " + factoid[3], original_status.id)
                    else:
                        self.api.tweet_reply(self.tweet_mentions(tweet) \
                            + "@" + tweet.user.screen_name + " " + factoid[3], tweet.id)
            return factoid
        else:
            self.log("No triggers found.")
            return False

    def add_fact(self, tweet):
        text = tweet.text
        text = text.replace("@cuddle_bot", "") # strip out @bot_name

        if "@" in text:
            return False # ignore if it contains mentions

        parsed = text.split(' ')

        # lets try learning everything oh god this is probably a bad idea
        if True: #parsed[0] == self.bot_name:

            # check if it is a cuddle request
            # TODO move this into a method
            if len(parsed) >= 2 and parsed[0] == "cuddle":
                if parsed[1][0] == "@":
                    self.api.tweet_reply("@" + tweet.user.screen_name \
                        + " * cuddles " + parsed[1], tweet.id) + " *"
                    self.log("User successfully cuddled")
                    return True
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
                if len(pre.split(" "))>2 and len(post)>0:
                    # remove trailing space
                    pre  = pre[:len(pre)-1]
                    post = post[:len(post)-1]

                    self.db.add_factoid("fact", pre, post, "is", 0, "@" + tweet.user.screen_name)
                    return True

    def random_factoid(self, tweet):
        if tweet.text == "@cuddle_bot say something random":
            factoid = self.db.get_random_factoid()
            if factoid:
                self.api.tweet_reply("@" + tweet.user.screen_name + " " \
                    + factoid[2] + " " + factoid[4] + " " + factoid[3], tweet.id)
            return True
        else:
            return False

    def provide_help(self, tweet):
        if tweet.text == (self.bot_name + " --help"):
            self.api.tweet_reply("@" + tweet.user.screen_name \
                + " My documentation is here: https://t.co/xmPavDZWxY", tweet.id)
            return True
        else:
            return False
