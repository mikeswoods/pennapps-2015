import cv2, sys, tempfile

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

frames = []
ret = 1 #initialize
while ret:  # note that we don't have to use frame number here, we could read from a live written file.
    if count % frame_iter == 0:
    	ret, frame = vidFile.read() # read first frame, and the return code of the function.
    	temp = tempfile.NamedTemporaryFile()
    	frames.append(temp.name)
    	print frame
    	print count, temp.name
    else:
    	ret = vidFile.grab()
    #cv2.imshow("frameWindow", frame)
    #cv2.waitKey(int(1/fps*1000)) # time to wait between frames, in mSec
    count += 1
    # ret, frame = vidFile.read() # read next frame, get next return code
print count