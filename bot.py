# Frank Zhao 2014
# <frank@frankzhao.net>

import tweepy
import re
import database
import twitterapi

db = database.Database()
bot_name = "@cuddle_bot"

# Counters
factoid_count = 0
inventory_count = 0

# Initalise Twitter
twitter_api = twitterapi.TwitterApi()
twitter = twitter_api.connect()
# mentions = twitter.mentions_timeline()
# user = mentions[0].author.screen_name

def log(msg):
    print "LOG (BOT): " + msg

while True:
    # Quote parsing
    # syntax is "@bot remember @user some quote"
    tweet = raw_input("Enter some text: ")
    parsed = re.split(' ', tweet)
    
    if tweet == "@" + bot_name + " remember this":
        quote_tweet = twitter.get_status(tweet.in_reply_to_status_id)
        quotee = quote_tweet.user.screen_name
        quote  = quote_tweet.text
        db.add_factoid("quote", "quote " + quotee, quote, "remember", 0, quotee)
    elif not len(parsed) < 4:
        # are we creating a quote?
        if (parsed[0] == bot_name and parsed[1] == "remember"):
            quotee = re.split(' ', re.findall("remember @[^\s]+", tweet)[0])[1]
            quote = re.split("@[^\s]+ ", tweet)
            if len(quote) == 3:
                quote = re.split("@[^\s]+ ", tweet)[2]
                db.add_factoid("quote", "quote " + quotee, quote, "remember", 0, quotee)
            else: log("Ignored invalid quote insertion: " + tweet)
        
        # specific quote retrival
        elif (parsed[0] == bot_name and parsed[1] == "quote"):
          db.get_quote(parsed[2], re.split("@[^\s]+ ", tweet)[2])
        
        #otherwise ignore
        else: log("Ignored invalid quote operation: " + tweet)
    
    # random quote retrival
    elif len(parsed) == 3:
        if (parsed[0] == bot_name and parsed[1] == "quote"):
            db.get_quote(parsed[2])
            
        
    # otherwise ignore
    else: log("Ignored invalid quote operation: " + tweet)