from PIL import Image
from math import cos, sin
from enum import IntEnum

alim = 50

class Direction(IntEnum):
    BOT = 0
    RIGHT = 1
    TOP = 2
    LEFT = 3

def inc(a): return a + 1
def dec(a): return a - 1
def nothing(a): return a

VISION = [
    (nothing, inc),
    (inc, nothing),
    (nothing, dec),
    (dec, nothing)
]

VISION_DIAG = [
    (dec, inc),
    (inc, inc),
    (inc, dec),
    (dec, dec)
]

def changePos(x, y, index, val=VISION):
    new = val[index]
    return (new[0](x), new[1](y))

backward = 0
moveList = []
def detectEdge(img: Image, x, y, direction: Direction, width, height) -> Direction:
    global backward, moveList
    straight = changePos(x, y, direction)
    left = changePos(x, y, (direction + 1) % 4)
    right = changePos(x, y, (direction + 3) % 4)

    sa = 0
    la = 0
    ra = 0
    if (straight[0] < 0  or straight[0] >= width or straight[0] >= height or straight[1] >= width or straight[1] >= height or straight[1] < 0):
        pass
    else:
        _,_,_,sa = img.getpixel(straight)
    if (left[0] < 0  or left[0] >= width or left[0] >= height or left[1] >= width or left[1] >= height or left[1] < 0):
        pass
    else:
        _,_,_,la = img.getpixel(left)
    if (right[0] < 0  or right[0] >= width or right[0] >= height or right[1] >= width or right[1] >= height or right[1] < 0):
        pass
    else:
        _,_,_,ra = img.getpixel(right)
    
    if (not backward and sa < alim and ra < alim and la < alim):
        backward = 1
        moveList.append((direction + 2) % 4)
        return (direction + 2) % 4

    if (sa < alim and ra < alim):
        backward = 0
        moveList.append((direction + 1) % 4)
        return (direction + 1) % 4
    if (sa < alim and la < alim):
        backward = 0
        moveList.append((direction + 3) % 4)
        return (direction + 3) % 4

    dleft = changePos(x, y, (direction + 1) % 4, VISION_DIAG)
    dright = changePos(x, y, (direction + 3) % 4, VISION_DIAG)

    dla = 0
    dra  = 0
    if (dleft[0] < 0  or dleft[0] >= width or dleft[0] >= height or dleft[1] >= width or dleft[1] >= height or dleft[1] < 0):
        pass
    else:
        _,_,_,dla = img.getpixel(dleft)
    if (dright[0] < 0  or dright[0] >= width or dright[0] >= height or dright[1] >= width or dright[1] >= height or dright[1] < 0):
        pass
    else:
        _,_,_,dra = img.getpixel(dright)

    if (sa > alim and ra > alim and dla < alim):
        backward = 0
        moveList.append((direction + 3) % 4)

        return (direction + 3) % 4

    if (sa > alim and la > alim and ra > alim and dra < alim):
        backward = 0
        moveList.append((direction + 3) % 4)
        return (direction + 3) % 4
    
    if (sa > alim and la > alim and ra > alim and dla < alim):
        backward = 0
        moveList.append((direction + 1) % 4)
        return (direction + 1) % 4
    

    if (sa < alim and la > alim and ra > alim and dla < alim):
        backward = 0
        moveList.append((direction + 3) % 4)
        return (direction + 3) % 4
    
    if (sa < alim and la > alim and ra > alim and dra < alim):
        backward = 0
        moveList.append((direction + 1) % 4)
        return (direction + 1) % 4
    
    if (backward and sa > alim and ra > alim and dra < alim):
        backward = 0
        moveList.append((direction + 3) % 4)
        return (direction + 3) % 4

    return direction

def findDirection(img: Image, x, y, direction = Direction) -> Direction | None:
    t = changePos(x, y, 0)
    r = changePos(x, y, 1)
    b = changePos(x, y, 2)
    l = changePos(x, y, 3)

    _,_,_,top = img.getpixel(t)
    _,_,_,right = img.getpixel(r)
    _,_,_,bottom = img.getpixel(b)
    _,_,_,left = img.getpixel(l)

    if(top < alim and right < alim):
        return direction.BOT
    if(right < alim and bottom < alim):
        return direction.RIGHT 
    if(bottom < alim and left < alim):
        return direction.TOP
    if(top < alim and left < alim):
        return direction.LEFT
    return None

def isTranparent(img: Image, x, y):
    _,_,_,a = img.getpixel((x, y))
    return a < alim

def findFirstEdge(img: Image, width, height):
    for x in range(width):
        for y in range(height):
            if (isTranparent(img, x, y)):
                return (x, y)
    return (0, 0)

def findAllEdge(img: Image, outline: list):
    width, height = img.size
    actual = None
    start = findFirstEdge(img, width, height)
    
    if (not start):
        return 0
    
    x, y = start
    
    direction = Direction.BOT
    oldDirection = direction

    outline.append((x,y))
    actual = None

    while (start != actual):
        if not actual:
            actual = start
        x, y = actual
        direction = detectEdge(img, x, y, direction, width, height)
        if (oldDirection != direction and actual not in outline):
            outline.append(actual)
        oldDirection = direction
        actual = changePos(x, y, direction)
    
    return 1

