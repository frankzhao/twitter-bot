# Frank Zhao 2014
# <frank@frankzhao.net>
# Database methods

import sqlite3
from random import randint

db_connection = sqlite3.connect('db/bot.db') # Connect to db
db = db_connection.cursor() # Database cursor

class Database:
    def log(self, msg):
        print "LOG (DB): " + msg
    
    # Sets up the initial database
    def init(self):
        # Create factoid table
        db.execute('''
            CREATE TABLE IF NOT EXISTS `factoids` (
              `id` INTEGER PRIMARY KEY NOT NULL,
              `kind` TEXT default NULL,
              `trigger` TEXT default NULL,
              `value` TEXT default NULL,
              `verb` TEXT default NULL,
              `protected` int NOT NULL,
              `user` TEXT default NULL
            )''')
    
        # Create inventory table
        db.execute('''
            CREATE TABLE IF NOT EXISTS `inventory` (
              `id` INTEGER PRIMARY KEY NOT NULL,
              `value` TEXT default NULL,
              `user` TEXT default NULL
            )''')
    
        # Create variable types table
        db.execute('''
            CREATE TABLE IF NOT EXISTS `variables` (
              `id` INTEGER PRIMARY KEY NOT NULL,
              `kind` TEXT default NULL,
              `value` TEXT default NULL,
              `protected` int NOT NULL
            )''')
    
        # Create variables table
        db.execute('''
            CREATE TABLE IF NOT EXISTS `vars` (
              `id` INTEGER PRIMARY KEY NOT NULL,
              `kind` TEXT default NULL,
              `value` TEXT default NULL
            )''')
            
        # Create seen tweets table
        db.execute('''
            CREATE TABLE IF NOT EXISTS `tweet_id` (
              `id` INTEGER PRIMARY KEY NOT NULL,
              `tweet_id` TEXT default NULL
            )''')
        db.execute('''
            INSERT INTO `tweet_id` (
                `tweet_id`
            ) VALUES (?)
            ''', ('0', ))
        db_connection.commit()
        print "Database initialised"

    def update_latest_seen_tweet_id(self, tweet_id):
        db.execute('''
            UPDATE `tweet_id`
            SET tweet_id=?
            WHERE id=1
            ''', (tweet_id, ))
        db_connection.commit()
    
    def get_latest_seen_tweet_id(self):
        row = db.execute('''
            SELECT * FROM `tweet_id` 
            WHERE id=1
            ''')
        return int(row.fetchone()[1])

    def add_variable(self, kind, value, protected):
        row = [kind, value, protected]
        db.execute('''
            INSERT INTO `variables` (
                `kind`, `value`, `protected`
            ) VALUES (?, ?, ?)
            ''', row)
        db_connection.commit()
        print "VARIABLE: Added new variable \'" + value + "\' as a <" + kind + ">"

    def add_factoid(self, kind, trigger, value, verb, protected, user):
        row = [kind, trigger, value, verb, protected, user]
        db.execute('''
            INSERT INTO `factoids` (
                `kind`, `trigger`, `value`, `verb`, `protected`, `user`
            ) VALUES (?, ?, ?, ?, ?, ?)
            ''', row)
        db_connection.commit()
        self.log("FACTOID: added <" + trigger + "> <" + verb + "> <" \
            + value + "> as a <" + kind + "> for user " + user)

    def retrieve_all(self, table):
        for row in db.execute("SELECT * FROM " + table):
            print row
            
    # retrieve a random value from an iterable
    def retrieve_random(self, iterable, n):
        i=0
        randi = randint(0,n-1)
        for value in iterable:
            if i == randi:
                return value
                break
            else:
                i += 1
    
    def delete_entry(self, table, idn):
        db.execute("DELETE FROM " + table + " WHERE id=" + str(idn))
        self.log("Entry deleted from " + table + "!")
    
            
    def get_quote(self, user, keywords=''):
        # remove @ from user
        user = user[1:]
        if keywords:
            self.sanitize(keywords)
            quotes = db.execute('''
                SELECT * FROM `factoids` 
                WHERE kind='quote' 
                AND user=? 
                AND value LIKE ?''', (user, '%'+keywords+'%'))
            quote = quotes.fetchone()
            return quote
        else:
            # Have a look at all the quotes for user
            self.log("Getting quote for " + user)
            n = db.execute("SELECT COUNT(*) FROM `factoids` WHERE kind='quote' AND user=?",\
                (user,)).fetchone()[0]
            self.log("Found " + str(n) + " quotes from " + user)
            if n>0:
                randi = randint(0,n-1)
                # Select a random quote
                quotes = db.execute('''
                    SELECT * FROM `factoids` 
                    WHERE kind='quote' 
                    AND user=?''', (user,))
                return self.retrieve_random(quotes, n)
            else: return None
            
    # TODO clean this up
    def get_factoid(self, text):
        
        rows = db.execute("SELECT * FROM `factoids`")
        factoids = rows.fetchall()
        
        matches = []
        
        for factoid in factoids:
            if factoid[2] in text:
                matches.append(factoid)

        if len(matches)>0:
            return matches[randint(0, len(matches)-1)]
        else: return None