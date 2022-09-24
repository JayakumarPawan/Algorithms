import random
import time
STRIPTIME = 0
def bruteforce(points, left, right):
    mindist = 99999999999999
    for i in range(left,right):
        for j in range(i+1,right):
            distance = dist(points[i], points[j])
            if distance < mindist:
                mindist = distance
    return mindist

def recursive(points,ypoints, left , right):
    size = right - left
    if size <= 15:
        return bruteforce(points, left, right)
    mid = left + size//2
    lefth,righth = [],[]
    for point in ypoints:
        if point[0] <points[mid][0]:
            lefth.append(point)
        else:
            righth.append(point)

    dl = recursive(points,lefth,left,mid)
    dr = recursive(points,righth,mid,right)
    d = min(dl,dr)

    bound = points[mid][0]
    strip = []
    for i in range(len(ypoints)):
        if abs(ypoints[i][0] - bound) < d:
            strip.append(ypoints[i])

    return stripClosest(strip, d)

def stripClosest(points, d):
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            distance = dist(points[j], points[i])
            if distance < d:
                d = distance
    return d


def dist(p1,p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def evaluate():
    points = []
    while True:
        inp = input()
        if inp == '0':
            exit()
        if inp.find(' ') == -1:
            num_points = int(inp)
        else:
            sep = inp.find(' ')
            points.append((float(inp[:sep]),float(inp[sep+1:])))
            num_points-=1
            if num_points == 0:
                points.sort()
                ypoints = sorted(points,key=lambda x: x[1])
                mindist = recursive(points,ypoints,0, len(ypoints))
                #mindist = bruteforce(points,0,len(points))    
                points = []
                if mindist > 10000:
                    print('infinity')
                else:
                    print("{:.4f}".format(round(mindist, 4)))

def compare():
    points = []
    numpoints  =1000
    for i in range(numpoints):
        points.append( (random.uniform(-50000,50000),random.uniform(-50000,50000))) 
        #print(str(points[i][0]) + " " + str(points[i][1]))
    points.sort()
    ypoints = sorted(points,key=lambda x: x[1])
    mindist = bruteforce(points, 0, len(points))
    mindist2 = recursive(points,ypoints,0, len(ypoints))
    print("\n{:.4f}".format(round(mindist, 4)))
    print("{:.4f}".format(round(mindist2, 4)))

#compare()
evaluate()