import engine
import engine.read
import engine.images
import engine.match
import numpy as np
from random import choice, randint
from scipy import spatial
import skimage
from skimage.transform import rescale
import sqlite3

################################################################################

def create(input_image, output_name='output_', k=5, window=(16,16), n=1):

    #icons    = engine.images.load("data/icons/*.png")
    db_stats = engine.images.read_db()

    (tree,filenames) = engine.match.build_index(db_stats)

    I = engine.read.load_image(input_image)

    for m in range(0,n):

        print "> composite iter: {}".format(m)

        (bins,colors) = engine.read.resample(I, window, jitter=(5,5))
        J = np.zeros_like(I)
        
        for ((xy1,xy2), avg_color) in zip(bins,colors):

            (x1,y1) = xy1
            (x2,y2) = xy2
            (dists, indices) = tree.query(avg_color, k=k)

            i      = randint(0, len(dists)-1)
            DIST   = dists[i]
            INDEX  = indices[i]
            CHOSEN = filenames[INDEX]

            X = engine.read.load_image("data/icons/"+CHOSEN)
            (iw,ih,id) = X.shape
            xscale = float(window[0]) / float(iw)
            yscale = float(window[1]) / float(ih)
            scale_factor = (xscale, yscale)

            Y = skimage.img_as_ubyte(rescale(X, scale_factor))

            if (x2 - x1) == window[0] and (y2 - y1) == window[1]:

                J[x1:x2,y1:y2,:] = Y[:,:,0:3] # Exclude alpha channel

        skimage.io.imsave('{}{}.png'.format(output_name, m), J)
