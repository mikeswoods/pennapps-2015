from os.path import abspath
import sys, sqlite3, threading, imp

engine = abspath('../')
sys.path.append(engine)

import engine
import engine.mosaic

print engine.DB_FILE

def job():
    db = sqlite3.connect('image.db')
    c = db.cursor()
    c.execute("SELECT * FROM images WHERE modified IS NULL")
    unmodded = c.fetchall()
    for u in unmodded:
        print u[1]
        old_file = u[1]
        f = u[1].split("/")
        f[2] = "mod_"+f[2]
        new_file = "/".join(f)
        print new_file
        engine.mosaic.create(old_file,new_file,k=3,n=10,start_window=160)
    threading.Timer(10,job).start()

job()