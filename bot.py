# Frank Zhao 2014
# <frank@frankzhao.net>

import twitter
import re
import database

db = database.Database()

# Counters
factoid_count = 0
inventory_count = 0

def log(msg):
    print "LOG: " + msg

while True:
    # syntax is "@bot quote @user some quote"
    tweet = raw_input("Enter some text: ")
    # check that the bot has been mentioned
    parsed = re.split(' ', tweet)
    if not len(parsed) < 4:
        if (parsed[0] == "@bot" and parsed[1] == "quote"):
            quotee = re.split(' ', re.findall("quote @[^\s]+", tweet)[0])[1]
            quote = re.split("@[^\s]+ ", tweet)
            if len(quote) == 3:
                quote = re.split("@[^\s]+ ", tweet)[2]
                db.add_factoid("quote", "quote " + quotee, quote, "quote", 0, "@user")
            else: log("Ignored invalid quote: " + tweet)
        else: log("Ignored invalid quote: " + tweet)
    else: log("Ignored invalid quote: " + tweet)