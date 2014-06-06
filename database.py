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
        db_connection.commit()
        print "Database initialised"

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
        print "FACTOID: added <" + trigger + "> <" + verb + "> <" \
            + value + "> as a <" + kind + "> for user " + user

    def retrieve_all(self, table):
        for row in db.execute("SELECT * FROM " + table):
            print row
            
    def get_quote(self, user, keywords=''):
        if keywords:
            quotes = db.execute('''
                SELECT * FROM `factoids` 
                WHERE kind='quote' 
                AND user=? 
                AND value LIKE ?''', (user, '%'+keywords+'%'))
            quote = quotes.fetchone()
            print quote
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
                i = 0
                for quote in quotes:
                    if i == randi:
                        print quote
                        break
                    else:
                        i += 1