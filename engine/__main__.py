import engine
import engine.mosaic
from os import getcwd
from os.path import join, basename, realpath
import sys

################################################################################

if len(sys.argv) != 2:
    raise "Expected input file"

#input  = engine.TEST_IMAGES[6]
input  = realpath(join(getcwd(), sys.argv[1]))
output = join(getcwd(), 'mosaic_' + basename(input))

if engine.mosaic.is_video_file(input):
    output += ".gif"

# input  = engine.TEST_VIDEOS[0]
# output = join(getcwd(), 'mosaic_' + basename(input)) + ".gif"

print "<INPUT> {}\n<OUTPUT> {}".format(input, output)

engine.mosaic.create(input, output, k=3, n=12)

################################################################################
