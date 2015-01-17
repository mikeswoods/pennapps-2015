import engine
import engine.mosaic
from os import getcwd
from os.path import join, basename

################################################################################

input_image  = engine.TEST_IMAGES[0]
output_image = join(getcwd(), 'mosaic_' + basename(input_image))

print "<INPUT> {}\n<OUTPUT> {}".format(input_image, output_image)

engine.mosaic.create(input_image, output_image, k=4, n=12, start_window=120, end_window=8)

################################################################################
