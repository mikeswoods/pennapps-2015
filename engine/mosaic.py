import engine
import engine.read
import engine.images
import engine.match
import numpy as np
from random import choice, randint
from scipy import spatial
import skimage
from skimage.io import imsave
from skimage.transform import rescale
import sqlite3
from PIL import Image


################################################################################

def create_single(I, k=5, window=(16,16), jitter_amt=10):

    #icons    = engine.images.load("data/icons/*.png")
    db_stats = engine.images.read_db()

    (tree,filenames) = engine.match.build_index(db_stats)

    (bins,colors) = engine.read.resample(I, window, jitter=(jitter_amt,jitter_amt))
    (w,h,_) = I.shape
    J = np.zeros((w,h,4)).astype(np.uint8) # RGBA of uint8
    
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

            J[x1:x2,y1:y2,:] = Y # Copy all channels (R,G,B, and A)

    return J

def composite(base_img, paste_img):
    layer = Image.fromarray(paste_img)
    # see http://pillow.readthedocs.org/en/latest/reference/Image.html#PIL.Image.Image.paste
    base_img.paste(layer, box=(0,0), mask=layer)
    return base_img

def create(input_image, k=5, window=(16,16), jitter_amt=10, n=1):

    I = engine.read.load_image(input_image)
    (w,h,_) = I.shape

     # Blank w x h image with 4 color channels: RGBA
    base = np.zeros((w,h,4)).astype(np.uint8)
    base[:,:,0] = np.uint8(255)
    base[:,:,2] = np.uint8(255)
    base[:,:,3] = np.uint8(255)

    imsave("base.png", base)

    base_img = Image.fromarray(base)

    for i in range(0,n):

        print ">> Compositing layer: {}".format(i)

        layer_img = create_single(I, k=k, window=window, jitter_amt=jitter_amt)
        imsave("layer_{}.png".format(i), layer_img)

        base_img = composite(base_img, layer_img)

    imsave("output.png", base_img)

