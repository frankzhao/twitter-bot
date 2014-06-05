# Frank Zhao 2014
# <frank@frankzhao.net>

import twitter
import sqlite3

db_connection = sqlite3.connect('db/bot.db') # Connect to db
db = db_connection.cursor() # Database cursor

# Sets up the initial database
def init():
    # Create factoid table
    db.execute('''
        CREATE TABLE `factoids` (
          `id` INTEGER PRIMARY KEY NOT NULL,
          `kind` TEXT default NULL,
          `value` TEXT default NULL,
          `protected` int NOT NULL,
          `user` TEXT default NULL
        )''')
        
    # Create inventory table
    db.execute('''
        CREATE TABLE `inventory` (
          `id` INTEGER PRIMARY KEY NOT NULL,
          `value` TEXT default NULL,
          `user` TEXT default NULL
        )''')
        
    # Create variable types table
    db.execute('''
        CREATE TABLE `variables` (
          `id` INTEGER PRIMARY KEY NOT NULL,
          `kind` TEXT default NULL,
          `value` TEXT default NULL,
          `protected` int NOT NULL
        )''')
        
    # Create variables table
    db.execute('''
        CREATE TABLE `vars` (
          `id` INTEGER PRIMARY KEY NOT NULL,
          `kind` TEXT default NULL,
          `value` TEXT default NULL
        )''')
    db_connection.commit()
    
def add_variable(kind, value, protected):
    row = [kind, value, protected]
    db.execute('''
        INSERT INTO `variables` (
            `kind`, `value`, `protected`
        ) VALUES (?, ?, ?)
        ''', row)
    db_connection.commit()

def retrieve_all(table):
    for row in db.execute("SELECT * FROM " + table):
        print row

        