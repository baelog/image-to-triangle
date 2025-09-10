import math
 
def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang
 

def IsInMiddle(A, B, C):
    AB = ((A[0] - B[0]) * (A[0] - B[0])) + ((A[1] - B[1]) * (A[1] - B[1]))
    BC = ((B[0] - C[0]) * (B[0] - C[0])) + ((B[1] - C[1]) * (B[1] - C[1]))
    AC = ((A[0] - C[0]) * (A[0] - C[0])) + ((A[1] - C[1]) * (A[1] - C[1]))

    if (AB == BC + AC):
        return C
    if (BC == AB + AC):
        return A
    if (AC == BC + AB):
        return B
    return 0

def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def PointInTriangle(pt,  v1,  v2, v3):

    d1 = sign(pt, v1, v2);
    d2 = sign(pt, v2, v3);
    d3 = sign(pt, v3, v1);

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0);
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0);

    return not (has_neg and has_pos)

def pointListInTirangle(pointList, p1, p2, p3):
    for point in pointList:
        if (point is p1 or point is p2 or point is p3):
            continue
        if (PointInTriangle(point, p1, p2, p3)):
            return True
    return False

def createTriangle(pointList):
    tri = []
    llen = len(pointList)
    while (llen > 3):
        last = [ i for i in pointList]

        for i in range(llen):
            p1 = pointList[(llen + i - 1) % llen]
            p2 = pointList[i]
            p3 = pointList[(i + 1) % llen]
            ang = getAngle(p1, p2, p3)
            if (ang == 0):
                if ((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]) < (p3[0] - p2[0]) * (p3[0] - p2[0]) + (p3[1] - p2[1]) * (p3[1] - p2[1])):
                    pointList.pop((llen + i - 1) % llen)
                else:
                    pointList.pop((i + 1) % llen)
                break
            if (ang == 180):
                pointList.pop(i)
                break
            if (ang > 180):
                continue
            if pointListInTirangle(pointList, p1, p2, p3):
                continue
            tri.append((p1, p2, p3))
            pointList.pop(i)
            break
        llen = len(pointList)
        if len(pointList) == len(last):
            return tri
    
    tri.append((pointList[0], pointList[1], pointList[2]))
    return tri

