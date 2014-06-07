# Frank Zhao 2014
# <frank@frankzhao.net>

import time
import tweepy
import re
import database
import twitterapi
import interactions
from datetime import datetime

db = database.Database()
bot_name = "@cuddle_bot"

# Counters and timers
factoid_count = 0
inventory_count = 0
last_seen_tweet_id = db.get_latest_seen_tweet_id()
sleep_interval = 100 # seconds

# Initalise Twitter
twitter_api = twitterapi.TwitterApi()
twitter = twitter_api.connect()
# mentions = twitter.mentions_timeline()
# user = mentions[0].author.screen_name

interaction = interactions.Interactions(twitter_api, twitter, db, bot_name)

def log(msg):
    print "LOG (BOT): " + msg

def main(timeline):
    global last_seen_tweet_id
    if len(timeline) == 0:
        log("No tweets found in timeline!")
    else:
        for tweet in timeline:
            if (int(tweet.id) > last_seen_tweet_id) and ("@" + tweet.user.screen_name) != bot_name:
                log("Processing: " + tweet.text)
                
                # learn facts
                interaction.add_fact(tweet)
                
                # Things to run regardless of tweet format
                # Cuddles and triggers
                if not interaction.process_quote(tweet):
                    # look for quotes
                    interaction.triggers(tweet)
                
                # This block handles all tweets with @bot_name as the first word
                elif (re.split(' ', tweet.text)[0] == bot_name):
                    pass
                    
                # This block handles all other tweets not beginning with @bot_name
                else: 
                    pass
                
                # update id of last seen tweet
                last_seen_tweet_id = tweet.id
                db.update_latest_seen_tweet_id(tweet.id)

            else:
                log("Ignoring already processed tweet.")

db.init()        
while True:
    #break
    
    # keep track of last seen tweet even after restart
    last_seen_tweet_id = db.get_latest_seen_tweet_id()
    
    # Retrieve mentions
    mentions = twitter.mentions_timeline()
    mentions.reverse()
    log("Retrieved mentions...")
    
    # start executing mentions timeline functions
    main(mentions)
    
    # Retrieve timeline
    timeline = twitter.home_timeline()
    timeline.reverse()
    log("Retrieved timeline...")
    
    # start executing home timeline functions
    main(timeline)
    
    log("Going into idle... " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
    time.sleep(sleep_interval)
    