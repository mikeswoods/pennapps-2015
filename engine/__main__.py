import engine
import engine.mosaic
from os import getcwd
from os.path import join, basename

################################################################################

input_image  = engine.TEST_IMAGES[3]
output_image = join(getcwd(), 'mosaic_' + basename(input_image))

print "<INPUT> {}\n<OUTPUT> {}".format(input_image, output_image)

engine.mosaic.create(input_image, output_image, k=3, n=10, start_window=160)

################################################################################
