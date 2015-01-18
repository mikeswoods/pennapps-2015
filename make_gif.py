import cv2, sys, tempfile
import engine.mosaic
from os.path import join, basename

try:
    vidFile = cv2.VideoCapture(sys.argv[1])
except:
    print "problem opening input stream"
    sys.exit(1)
if not vidFile.isOpened():
    print "capture stream not open"
    sys.exit(1)

nFrames = int(vidFile.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)) # one good way of namespacing legacy openCV: cv2.cv.*
print "frame number: %s" %nFrames
fps = vidFile.get(cv2.cv.CV_CAP_PROP_FPS)
print "FPS value: %s" %fps
frame_iter = nFrames/10 #30 frames returned
count = 0

emojified_frame_locations = []
ret = 1 #initialize
while ret:  # note that we don't have to use frame number here, we could read from a live written file.
    if count % frame_iter == 0:
        ret, frame = vidFile.read() # read first frame, and the return code of the function.
        temp = tempfile.NamedTemporaryFile(delete=False)
        print temp.name
        temp.name = temp.name + '.jpg'
        engine.mosaic.create(frame, temp.name)
        emojified_frame_locations.append(temp.name)
        print count, temp.name
        print emojified_frame_locations
    else:
        ret = vidFile.grab()
    #cv2.imshow("frameWindow", frame)
    #cv2.waitKey(int(1/fps*1000)) # time to wait between frames, in mSec
    count += 1
    # ret, frame = vidFile.read() # read next frame, get next return code
print count