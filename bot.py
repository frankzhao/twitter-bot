# Frank Zhao 2014
# <frank@frankzhao.net>

import time
import tweepy
import re
import database
import twitterapi

db = database.Database()
bot_name = "@cuddle_bot"

# Counters and timers
factoid_count = 0
inventory_count = 0
sleep_interval = 300

# Initalise Twitter
twitter_api = twitterapi.TwitterApi()
twitter = twitter_api.connect()
# mentions = twitter.mentions_timeline()
# user = mentions[0].author.screen_name

def log(msg):
    print "LOG (BOT): " + msg

def main():
    # keep track of last seen tweet even after restart
    last_seen_tweet_id = db.get_latest_seen_tweet_id()
    
    # Quote parsing
    # syntax is "@bot remember @user some quote"
    #tweet = raw_input("Enter some text: ")
    mentions = twitter.mentions_timeline()
    mentions.reverse()
    log("Retrieved mentions...")
    if len(mentions) == 0:
        log("No mentions!")
    else:
        for tweet in mentions:
            if int(tweet.id) > last_seen_tweet_id:
                # update id of last seen tweet
                last_seen_tweet_id = tweet.id
                db.update_latest_seen_tweet_id(tweet.id)
                parsed = re.split(' ', tweet.text)
                
                log("Processing: " + tweet.text)
                
                if (bot_name + " remember this") in tweet.text:
                    quote_tweet = twitter.get_status(tweet.in_reply_to_status_id)
                    quotee = quote_tweet.user.screen_name
                    quote  = quote_tweet.text
                    db.add_factoid("quote", "quote " + quotee, quote, "remember", 0, quotee)
                    twitter_api.tweet_reply("Ok @" + tweet.user.screen_name + "!" \
                        + " (@" + quotee + ")", tweet.id)
                elif not len(parsed) < 4:
                    # are we creating a quote?
                    if (parsed[0] == bot_name and parsed[1] == "remember"):
                        quotee = re.split(' ', re.findall("remember @[^\s]+", tweet.text)[0])[1]
                        quote = re.split("@[^\s]+ ", tweet.text)
                        if len(quote) == 3:
                            quote = re.split("@[^\s]+ ", tweet.text)[2]
                            db.add_factoid("quote", "quote " + quotee, quote, "remember", 0, quotee)
                        else: log("Ignored invalid quote insertion: " + tweet.text)
        
                    # specific quote retrival
                    # syntax is @bot quote @user [keywords]
                    elif (parsed[0] == bot_name and parsed[1] == "quote"):
                      quote = db.get_quote(parsed[2], re.split("@[^\s]+ ", tweet.text)[2])
                      twitter_api.tweet_reply(quote[6] + ": " + quote[3], tweet.id)
        
                    #otherwise ignore
                    else: log("Ignored invalid quote operation: " + tweet.text)
    
                # random quote retrival
                elif len(parsed) == 3:
                    if (parsed[0] == bot_name and parsed[1] == "quote"):
                        quote = db.get_quote(parsed[2])
                        twitter_api.tweet_reply("@" + quote[6] + ": " + quote[3] \
                            + " (@" + tweet.user.screen_name + ")", tweet.id)
            
        
                # otherwise ignore
                else: log("Ignored invalid quote operation: " + tweet.text)
    
        log("Going into idle...")
        time.sleep(sleep_interval)

db.init()        
while True:
    main()
    