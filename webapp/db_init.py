import sqlite3

db = sqlite3.connect('image.db')
db.execute("CREATE TABLE images (id INTEGER PRIMARY KEY, original TEXT NOT NULL, email TEXT NOT NULL, modified TEXT)")