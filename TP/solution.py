from PIL import Image
import os

image=raw_input('enter image path:')
image=Image.open(image)

def fix(image):
    pixels=image.load()
    (width,height)=image.size
    for x in xrange(width):
        for y in xrange(height):
            (r,g,b,a)=pixels[x,y]
            if r>235 and g>235 and b>235:
                pixels[x,y]=(255,255,255,0)
            elif r<6 and g<6 and b<6:
                pixels[x,y]=(0,0,0,255)
    newPath=raw_input('enter new path:')
    image.save(newPath)
    print "Done!"

fix(image)