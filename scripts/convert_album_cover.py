"""convert_album.py formats square images to be printed on 4x6 prints for use on 4 inch coasters. """

# This script is used to convert a directory of square aspect ratio images to a directory of 4x6 photo print format
# images. These images are intended to be printed out as 4x6 photo prints then cut out and used as art on 4 inch
# coasters. This script will skip any of the source images that are not exact square ratios.
#
# Example: [python convert_album_cover.py ../art/source ../art/destination]

from os import listdir  # Used to get the files in a directory.
from math import ceil  # Used to get the ceiling when creating 4x6 height and width.
import sys  # Used to handle command line arguments.
from PIL import Image  # Used to generate a 4x6 image.

# Command line arguments.
source_dir = sys.argv[1]
destination_dir = sys.argv[2]

# Adding a slash to directory if missing.
if source_dir[-1] != "/":
    source_dir = source_dir + "/"
if destination_dir[-1] != "/":
    destination_dir = destination_dir + "/"

print("Building 4x6 images")

for filename in listdir(source_dir):
    image = Image.open(source_dir + filename)
    width, height = image.size
    if width != height:
        print(filename + ": is not a square, skipping image")
    else:
        print(filename + ": building 4x6 image")
        canvas_width = ceil(width * 12 / 7)
        canvas_height = ceil(height * 8 / 7)
        canvas = Image.new(mode="RGB", size=(canvas_width, canvas_height), color=(255, 255, 255))
        canvas.paste(image)
        canvas.save(destination_dir + filename)
