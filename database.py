# Frank Zhao 2014
# <frank@frankzhao.net>
# Database methods

import sqlite3

db_connection = sqlite3.connect('db/bot.db') # Connect to db
db = db_connection.cursor() # Database cursor

class Database:
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