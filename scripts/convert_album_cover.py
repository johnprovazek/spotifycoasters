from os import listdir # Used to get the files in a directory
from math import ceil # Used to get the ceiling when creating 4x6 height and width
from PIL import Image # Used to generate a 4x6 image

for filename in listdir("../albumart/originalcover/"):
    image = Image.open("../albumart/originalcover/" + filename)
    width, height = image.size
    if(width != height):
        print(filename + ": is not a square, skipping")
    else:
        c_width = ceil(width * 12/7)
        c_height = ceil(height * 8/7)
        canvas  = Image.new(mode = "RGB", size = (c_width, c_height), color = (255, 255, 255) )
        canvas.paste(image)
        canvas.save("../albumart/4x6prints/" + filename)