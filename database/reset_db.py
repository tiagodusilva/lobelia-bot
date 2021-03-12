import os
import sqlite3

if os.path.isfile('database/database.db'):
    os.remove('database/database.db')

conn = sqlite3.connect('database/database.db')
c = conn.cursor()

file = open('database/schema.sql',mode='r') 
# read all lines at once
schema = file.read()
c.executescript(schema)
del schema

conn.commit()
conn.close()
