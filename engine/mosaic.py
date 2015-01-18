import engine
import engine.read
import engine.images
import engine.match
import numpy as np
import math
from random import choice, randint, random
from scipy import spatial
import skimage
from skimage.io import imsave
from skimage.transform import rescale
import sqlite3
from PIL import Image
import warnings
import magic

################################################################################

def flip_coin(chance):
    return random() < chance

################################################################################

def create_single(I, window_size, jitter_amt, images=None, k=5):

    #icons    = engine.images.load("data/icons/*.png")
    db_stats = engine.images.read_db()

    window = (window_size,window_size)
    jitter = (jitter_amt,jitter_amt)

    (tree,filenames) = engine.match.build_index(db_stats)

    # Any parts of the mask that are 1 will be processed, otherwise nothing
    MASK = engine.match.build_mask(I)

    # bins: @i ((x1,y1),(x2,y2))
    # colors: @i average color for bin[i]
    # show: @i bin[i] is masked/not masked
    (bins, colors, show) = engine.read.resample(I, window, mask=MASK, jitter=jitter)
    (w,h,_) = I.shape

    J = np.zeros((w,h,4)).astype(np.uint8) # RGBA of uint8
    
    chance = max(1.0 - (1.0 / (0.5 * math.sqrt(window_size))), 0.3)
    print ">> Chance of output: {}".format(chance)

    for ((xy1,xy2), avg_color) in zip(bins, colors):

        #if not bool(show_bin):
        #    continue

        #if not flip_coin(0.9):
        if not flip_coin(chance):
            continue

        # Find the closest
        (x1,y1) = xy1
        (x2,y2) = xy2
        (dists, indices) = tree.query(avg_color, k=k)

        i      = randint(0, len(dists)-1)
        DIST   = dists[i]
        INDEX  = indices[i]
        CHOSEN = filenames[INDEX]

        if images is None:
            X = engine.read.load_image("data/icons/"+CHOSEN)
        else:
            X = images[CHOSEN]

        # Resize to the given window:
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


def blank(w,h, debug=False):

    I = np.zeros((w,h,4)).astype(np.uint8)
    I[:,:,3] = np.uint8(255)
    # If debug, color the bg magenta
    if debug:
        I[:,:,0] = np.uint8(255)
        I[:,:,2] = np.uint8(255)
    return I


def create_image(input_image, output_image, k=3, n=10, start_window=120, end_window=10, images=None, debug=False):
    """
    All-in-one compositing step for static image

    @param str|numpy.ndarray input_image: Input image, either a filename or ndarray
    @param str output_image: Output image name
    @param int k Top k similar images are chosen for a givem block
    @param int n Number of compositing iterations
    @param start_window 64 Ending image chunk block size
    @param int end_window Ending image chunk block size
    @param images None
    @param debug False
    @param dict(str:numpy.array) images: dict of precached images: None by default
    """
    with warnings.catch_warnings():

        warnings.simplefilter("ignore")

        # Did we get a numpy array?
        if isinstance(input_image, np.ndarray):
            I = input_image.astype(np.uint8)
        else:
            I = engine.read.load_image(input_image)

        (w,h,_) = I.shape

        # Blank w x h image with 4 color channels: RGBA
        base = blank(w, h, debug=True)

        if images is not None:
            print ">> Using cached images"

        print ">> Initial window: {}".format(start_window)

        if debug:
            imsave("debug_base.png", base)

        base_img     = Image.fromarray(I)
        window_steps = np.linspace(start_window, end_window, num=n).astype(int)

        for (i,window) in enumerate(window_steps, start=0):

            jitter_amt = int(window * 0.5)

            print ">> Compositing layer: {}, window: {}, jitter: {}".format(i, window, jitter_amt)

            layer_img = create_single(I, window, jitter_amt, images=images, k=k)

            window = int(window * 0.75)

            if debug:
                imsave("debug_layer_{}.png".format(i), layer_img)

            base_img = composite(base_img, layer_img)

        imsave(output_image, base_img)


################################################################################

def create(input_image, *args, **kwargs):
    """
    Creates a mosaic for either an image or video

    @param str|numpy.ndarray input_image: Input image, either a filename or ndarray
    @param str output_image: Output image name
    @param int k Top k similar images are chosen for a givem block.
    @param int n Number of compositing iterations
    @param start_window 64 Ending image chunk block size
    @param int end_window Ending image chunk block size
    @param images None
    @param debug False
    @param dict(str:numpy.array) images: dict of precached images: None by default
    """
    if isinstance(input_image, np.ndarray):
        return create_image(input_image, *args, **kwargs)
    else:

        media_type = magic.from_file(input_image).strip().lower()
        video_formats =  ['mp4', 'ogv', 'ogg', 'avi']

        if any([fmt in media_type for fmt in video_formats]):
            raise ValueError('Video not supported yet!!!!!!!!')
        else:
            return create_image(input_image, *args, **kwargs)
