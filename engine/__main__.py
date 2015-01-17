import engine
import engine.read
import engine.images
import engine.match
import numpy as np
from random import choice, randint
from scipy import spatial
import sqlite3

images   = engine.images.load("data/icons/*.png")
db_stats = engine.images.read_db()

(tree,filenames) = engine.match.build_index(db_stats)

I = engine.read.load_image(engine.TEST_IMAGES[1])
J = np.zeros_like(I)

(bins,colors) = engine.read.resample(I, (16,16))

k = 5

for ((xy1,xy2), avg_color) in zip(bins,colors):

    (x1,y1) = xy1
    (x2,y2) = xy2
    (dists, indices) = tree.query(avg_color, k=k)

    i     = randint(0, len(dists)-1)
    DIST  = dists[i]
    INDEX = indices[i]
    chosen_image = filenames[INDEX]

    X = images[chosen_image]
    J[x1:y1,x2:y2,:] = X[:,:,0:3] # Exclude alpha channel
