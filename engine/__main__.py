import engine
import engine.mosaic
from os import getcwd
from os.path import join, basename

################################################################################

input  = engine.TEST_IMAGES[5]
output = join(getcwd(), 'mosaic_' + basename(input))

#input  = engine.TEST_VIDEOS[0]
#output = join(getcwd(), 'mosaic_' + basename(input)) + ".gif"

print "<INPUT> {}\n<OUTPUT> {}".format(input, output)

engine.mosaic.create(input, output, k=3, n=12, start_window=64, end_window=10)
#engine.mosaic.create(input, output, k=3, n=2, start_window=64, end_window=40)

################################################################################
