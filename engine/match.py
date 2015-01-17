#!/usr/bin/env python

import engine
import scipy
from scipy import spatial
from scipy import ndimage
from skimage import filter
from skimage.color import rgb2gray
from skimage.morphology import reconstruction, convex_hull_image
from skimage.exposure import rescale_intensity
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


def build_mask(I):

    I = rescale_intensity(I)

    #J = ndimage.gaussian_filter(I, 1)
    J = I
    T = filter.threshold_otsu(J, nbins=16)
    K = ndimage.morphology.binary_fill_holes(J < T)
    K = ndimage.gaussian_filter(K, 2)
    #K = ndimage.morphology.binary_fill_holes(K)

    return rgb2gray(K)
    #return convex_hull_image(K)
