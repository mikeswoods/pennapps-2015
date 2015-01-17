#!/usr/bin/env python

import engine
import sqlite3
import numpy as np
from glob import glob
from os import walk, listdir, remove, getcwd
from os.path import exists, isfile, isdir, join, abspath, realpath, basename
import skimage
from skimage.io import ImageCollection, imread
import hashlib
try:
    import cPickle as pickle
except:
    import pickle


def get_images(pattern):
    return [(name, skimage.img_as_ubyte(imread(name))) for name in glob(pattern)]


def load(pattern):

    m = hashlib.md5()
    m.update(pattern)
    sig = m.hexdigest()

    cache_file = "{}/{}.bin".format(engine.CACHE_PATH, sig)

    if not exists(cache_file):
        print "> Caching file: {}".format(cache_file)
        with open(cache_file, 'w') as f:
            image_data = dict([(basename(filename), im) for (filename, im) in get_images(pattern)])
            pickle.dump(image_data, f)
    else:
        print "> Loading file: {}".format(cache_file)
        with open(cache_file, 'r') as f:
            image_data = pickle.load(f)

    return image_data


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


def read_db():
    conn = sqlite3.connect(engine.DB_FILE)
    c = conn.cursor()
    c.execute("SELECT filename, red, green, blue FROM images")
    rows = c.fetchall()
    conn.close()
    return rows

def store(conn, filename, image):
    stats = image_stats(image)

    c = conn.cursor()
    c.execute("INSERT INTO images(filename, red, green, blue) VALUES (?,?,?,?)"\
             ,(filename, int(stats[0]), int(stats[1]), int(stats[2])))


if __name__ == "__main__":

    if exists(engine.DB_FILE):
        print "> Removing {}".format(engine.DB_FILE)
        remove(engine.DB_FILE)

    conn = sqlite3.connect(engine.DB_FILE)
    create_db(conn)

    for (filename, image) in get_images("../data/icons/*.png"):
        print basename(filename)
        store(conn, basename(filename), image)

    conn.commit()
    conn.close()

    print "Done"
