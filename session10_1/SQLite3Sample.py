"""
This is a basic SQLite3 Python implementation, to initialise two tables.
The goal is to provide a comparison against an SQLAlchemy implementation, 
to highlight the differences between using an ORM and a native SQL database in Python.
"""

import sqlite3 

# Create a connection() object representing the database.

conn = sqlite3.connect('databasesqlite.db')

"""After connecting and running this file, 
you should see the databasesqlite.db file in the same directory. 
"""

# The cursor is created after the connection, so execute() functions can be called with it with raw SQL.

c = conn.cursor()

c.execute("""
			CREATE TABLE if not exists Users
			(id INTEGER PRIMARY KEY ASC, 
			 name TEXT(20), 
			 insurance_id INTEGER)
		""")

c.execute("""
			CREATE TABLE if not exists Insurance
			(insurance_id INTEGER PRIMARY KEY, 
			claim_id INTEGER,
			FOREIGN KEY(insurance_id) REFERENCES Users(insurance_id))
		""")

c.execute("""
			INSERT INTO Users VALUES(4, 'minerva', 3)
		""")

c.execute("""
			INSERT INTO Insurance VALUES(3,12345)
		""")

# Save/commit the changes.
conn.commit()

# Make sure changes are committed or they will be lost.
conn.close()



