#!/usr/bin/env python

from random import randint
import sqlite3
import numpy as np
import skimage
from itertools import combinations
from skimage import io
from skimage.io import ImageCollection, imread, imsave, imshow

TEST_IMAGES = [
     '../test/158_1baby_face.jpg'
    ,'../test/120529-face-chew-230p.jpg'
    ,'../test/famous-face-dementia-617x416.jpg'
    ,'../test/white_powder_on_celebrity_faces.jpg'
]

def load_image(name):
    return imread(name) 

def clamp(i, limits):
    return min(max(i, limits[0]), limits[1])

def bins(I, window, jitter):
    (m,n)   = window
    (w,h,d) = I.shape
    (jx,jy) = jitter
    rx      = randint(-jx, jx)
    ry      = randint(-jy, jy)

    print (rx,ry)

    #return [((i,j), (min(i+m, w-1), min(j+n, h-1))) for i in range(0,w,m) for j in range(0,h,n)]
    xy = [(clamp(i+rx, (0,w-1)), clamp(j+ry, (0,h-1))) for i in range(0,w,m) for j in range(0,h,n)]
    return [((i,j), (min(i+m, w-1), min(j+n, h-1))) for (i,j) in xy]

def resample(I, window, jitter=(0,0)):
    J = np.zeros_like(I)
    B = bins(I, window, jitter)

    for (c1,c2) in B:
        print c1, c2
        (x1,y1) = c1
        (x2,y2) = c2
        X       = slice(x1, x2)
        Y       = slice(y1, y2)
        chunk   = I[X,Y,:]
        avgR    = np.average(chunk[:,:,0]).astype(np.uint8)
        avgG    = np.average(chunk[:,:,1]).astype(np.uint8)
        avgB    = np.average(chunk[:,:,2]).astype(np.uint8)

        J[X,Y,0] = avgR
        J[X,Y,1] = avgG
        J[X,Y,2] = avgB
    return J

if __name__ == "__main__":

    I = load_image(TEST_IMAGES[1])
    J1 = resample(I, (16,16), (3,3))
    J2 = resample(I, (16,16), (3,3))

    imsave('J1.png', J1)
    imsave('J2.png', J2)
