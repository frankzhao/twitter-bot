# Frank Zhao 2014
# <frank@frankzhao.net>

import twitter
import re
import database

db = database.Database()
bot_name = "@bot"

# Counters
factoid_count = 0
inventory_count = 0

def log(msg):
    print "LOG (BOT): " + msg

while True:
    # Quote parsing
    # syntax is "@bot remember @user some quote"
    tweet = raw_input("Enter some text: ")
    # check that the bot has been mentioned
    parsed = re.split(' ', tweet)
    if not len(parsed) < 4:
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
          quotee = re.split(' ', re.findall("remember @[^\s]+", tweet)[0])[1]
          db.get_quote
        
        #otherwise ignore
        else: log("Ignored invalid quote operation: " + tweet)
    
    # random quote retrival
    #else if len(parsed) == 3:
        
    # otherwise ignore
    else: log("Ignored invalid quote operation: " + tweet)