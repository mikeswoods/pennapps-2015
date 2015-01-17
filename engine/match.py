#!/usr/bin/env python

import engine
import engine.images
from scipy import spatial
import sqlite3
import numpy as np

def build_index(db_data):

    n         = len(db_data)
    points    = np.zeros((n,3))
    filenames = []

    for (i,(filename, red, green, blue)) in enumerate(db_data, start=0):
        points[i,:] = [red, green, blue]
        filenames.append(filename)

    tree = spatial.KDTree(points)

    return (tree, filenames)

