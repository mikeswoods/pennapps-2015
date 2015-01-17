#!/usr/bin/env python

from random import randint
import sqlite3
import numpy as np
import skimage
from itertools import combinations
from skimage import io
from skimage.io import ImageCollection, imread, imsave, imshow


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

    #return [((i,j), (min(i+m, w-1), min(j+n, h-1))) for i in range(0,w,m) for j in range(0,h,n)]
    xy = [(clamp(i+rx, (0,w-1)), clamp(j+ry, (0,h-1))) for i in range(0,w,m) for j in range(0,h,n)]
    return [((i,j), (min(i+m, w-1), min(j+n, h-1))) for (i,j) in xy]


def resample(I, window, mask=None, jitter=(0,0)):

    B      = bins(I, window, jitter)
    colors = np.zeros((len(B), 3))
    show   = np.zeros((len(B), 1))

    # Show all by default
    show[:,:] = 1

    for (i, (c1,c2)) in enumerate(B, start=0):

        (x1,y1) = c1
        (x2,y2) = c2
        X       = slice(x1, x2)
        Y       = slice(y1, y2)

        # Colors:
        color_chunk = I[X,Y,:]
        avgR        = np.average(color_chunk[:,:,0]).astype(np.uint8)
        avgG        = np.average(color_chunk[:,:,1]).astype(np.uint8)
        avgB        = np.average(color_chunk[:,:,2]).astype(np.uint8)
        colors[i,:] = [avgR, avgG, avgB]

        # Mask:
        if mask is not None:
            mask_chunk  = mask[X,Y]
            show[i]     = np.uint8(np.any(mask_chunk))

    return (B, colors, show)
