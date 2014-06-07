# Frank Zhao 2014
# <frank@frankzhao.net>

import time
import tweepy
import re
import database
import twitterapi
import interactions

db = database.Database()
bot_name = "@cuddle_bot"

# Counters and timers
factoid_count = 0
inventory_count = 0
sleep_interval = 100

# Initalise Twitter
twitter_api = twitterapi.TwitterApi()
twitter = twitter_api.connect()
# mentions = twitter.mentions_timeline()
# user = mentions[0].author.screen_name

def log(msg):
    print "LOG (BOT): " + msg

def main():
    interaction = interactions.Interactions(twitter_api, twitter, db, bot_name)
    # keep track of last seen tweet even after restart
    last_seen_tweet_id = db.get_latest_seen_tweet_id()
    
    # Retrieve timeline
    timeline = twitter.home_timeline()
    timeline.reverse()
    log("Retrieved timeline...")
    if len(timeline) == 0:
        log("No tweets found in timeline!")
    else:
        for tweet in timeline:
            # sanitize the tweet
            if (int(tweet.id) > last_seen_tweet_id) and ("@" + tweet.user.screen_name) != bot_name:
                log("Processing: " + tweet.text)
                
                # Things to run regardless of tweet format
                # Cuddles and triggers
                if not interaction.triggers(tweet):
                    # look for quotes
                    interaction.process_quote(tweet)
                
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
                log("No new tweets found.")

db.init()        
while True:
    #break
    main()
    log("Going into idle...")
    time.sleep(sleep_interval)
    