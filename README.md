twitter-bot
===========

Twitter bot (a work in progress). Stores quotes for later retrieval and learns facts that can be triggered by key phrases. A running demo is at https://twitter.com/cuddle_bot

Example Usage
-------------

Remember the last tweet: `@cuddle_bot remember this`

Quote someone: `@cuddle_bot quote @user`

Find a particular quote: `@cuddle_bot quote @user something in the quote`

Teach it a fact: `@cuddle_bot something is something else`

Ask me for advice: `@cuddle_bot give me advice on [...]`

Dependencies
------------

Requires `mysqlite3` and Python 2.7
python-tweepy is used for the Twitter API.
A database file is created in db/bot.db if it does not already exist.

Start the bot with `python bot.py`.

Files
-----

#### bot.py

The general running of the bot are in this file. It will retrieve timelines and distribute tweets with the specified methods. The variable `bot_name` should be set to the name of your bot.

#### database.py

Manages all the database methods such as lookup, retrival and insertion.

#### interactions.py

All tweets should be processed with methods here. All methods defined in this file should take two arguements, `self` and a `tweet`. The tweets should be parsed here before querying methods in `database.py`. Make sure methods in this file are appropriately called in `bot.py`.

#### twitterapi.py

Twitter API functions are implemented in this file. **Your API keys go here**.

