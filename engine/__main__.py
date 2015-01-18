import engine
import engine.mosaic
from os import getcwd
from os.path import join, basename

################################################################################

input_image  = engine.TEST_IMAGES[5]
output_image = join(getcwd(), 'mosaic_' + basename(input_image))

print "<INPUT> {}\n<OUTPUT> {}".format(input_image, output_image)

ZZ = engine.read.load_image(input_image)
print ZZ

engine.mosaic.create(ZZ, output_image, k=3, n=12, start_window=64, end_window=10)

################################################################################
