#!/usr/bin/env python

import sqlite3
import numpy as np
from glob import glob
from os import walk, listdir, remove, getcwd
from os.path import exists, isfile, isdir, join, abspath, realpath
import skimage
from skimage.io import ImageCollection, imread

DB_FILE = abspath("images.db")

def get_images(pattern):
    return [(name, skimage.img_as_ubyte(imread(name))) for name in glob(pattern)]
    #return ImageCollection(pattern, load_func=lambda f: imread(f).astype(np.uint8))

def image_stats(image):
    # image is expected to be composed of uint8s
    # Only consider pixels that are not totally transparent
    J   = image[image[:,:,3] > 0]
    avg = np.average(J, axis=0)
    return tuple(map(np.uint8, avg[0:3]))

def create_db(conn):

    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE images(id       INTEGER PRIMARY KEY AUTOINCREMENT
                           ,filename TEXT NOT NULL UNIQUE
                           ,red      INTEGER NOT NULL
                           ,green    INTEGER NOT NULL
                           ,blue     INTEGER NOT NULL
                           )
        """)

def store(conn, filename, image):

    stats = image_stats(image)

    c = conn.cursor()
    c.execute("INSERT INTO images(filename, red, green, blue) VALUES (?,?,?,?)"\
             ,(filename, int(stats[0]), int(stats[1]), int(stats[2])))

if __name__ == "__main__":

    if exists(DB_FILE):
        print "> Removing {}".format(DB_FILE)
        remove(DB_FILE)

    conn = sqlite3.connect(DB_FILE)
    create_db(conn)

    for (filename, image) in get_images("./icons/*.png"):
        print filename
        store(conn, filename, image)

    conn.commit()
    conn.close()

    print "Done"
