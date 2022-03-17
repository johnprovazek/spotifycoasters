from os import listdir # Used to get the files in a directory
from math import ceil # Used to get the ceiling when creating 4x6 height and width
from PIL import Image # Used to generate a 4x6 image
import sys # Used to handle command line arguments

# Usage: This script is used to convert a directory of square aspect ratio images to a
#        directory of 4x6 aspect ratio images. These images are intented to be printed 
#        as 4x6 prints and cut out and used as art on 4 inch coasters. This script will
#        skip source images if they are not an exact square.
# Example run: "python convert_album_cover.py ../art/source ../art/destination"

# Command line arguments
source_dir = sys.argv[1]
destination_dir = sys.argv[2]

# Adding a slash to directory if necessary
if source_dir[-1] != "/":
    source_dir = source_dir + "/"
if destination_dir[-1] != "/":
    destination_dir = destination_dir + "/"

for filename in listdir(source_dir):
    print(filename)
    image = Image.open(source_dir + filename)
    width, height = image.size
    if(width != height):
        print(filename + ": is not a square, skipping")
    else:
        c_width = ceil(width * 12/7)
        c_height = ceil(height * 8/7)
        canvas  = Image.new(mode = "RGB", size = (c_width, c_height), color = (255, 255, 255) )
        canvas.paste(image)
        canvas.save(destination_dir + filename)