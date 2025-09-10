from PIL import Image
import sys

import itertools
import struct

from triangle import createTriangle
from outline import findAllEdge


frontier = []
randPoint = []
pointWithTriangle = []
triangle = []

            
if (__name__ == "__main__") :

    with Image.open(sys.argv[1]) as img:

        outline = []
        findAllEdge(img, outline)

        width, height = img.size

        # create a file to show outline, may be slow
        # for x in range(width):
        #     for y in range(height):
        #         if ((x,y) in outline):
        #             img.putpixel((x,y), (0,255,0,255))
        # img.save("test2.png")

        triangle = createTriangle(outline)

        nbTriangle = len(triangle)

        export = list(itertools.chain(*triangle))
        export = list(itertools.chain(*export))

        s = struct.pack('<i' + 'i'*len(export), nbTriangle, *export)
        f = open(sys.argv[2],'wb')
        f.write(s)
        f.close()