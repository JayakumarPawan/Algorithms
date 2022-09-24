import pickle
import heapq, random, pickle, math, time
from math import pi, acos, sin, cos
from tkinter import *
from collections import deque
import sys

# def calc_edge_cost(y1, x1, y2, x2):
#    #
#    # y1 = lat1, x1 = long1
#    # y2 = lat2, x2 = long2
#    # all assumed to be in decimal degrees
#
#    # if (and only if) the input is strings
#    # use the following conversions
#
#    y1  = float(y1)
#    x1  = float(x1)
#    y2  = float(y2)
#    x2  = float(x2)
#    #
#    R   = 3958.76 # miles = 6371 km
#    #
#    y1 *= pi/180.0
#    x1 *= pi/180.0
#    y2 *= pi/180.0
#    x2 *= pi/180.0
#    #
#    # approximate great circle distance with law of cosines
#    #
#    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R
#    #
#
# def make_graph(nodes = "nodes.txt", node_city = "id-name.txt", edges = "edges.txt"):
#    nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost = {}, {}, {}, {}, {}
#    map = {}   # have screen coordinate for each node location
#
#    fileNodes = open(nodes, "r+")
#    for x in fileNodes.readlines():
#       temp = x.split(" ")
#       nodeLoc[temp[0]] = (temp[1], temp[2].strip())
#    fileNodes.close()
#
#    fileCities = open(node_city, "r+")
#    for y in fileCities.readlines():
#       y1 = y.strip()
#       temp1 = [y1[0:7], y1[8:len(y1)]]
#       nodeToCity[temp1[0]] = temp1[1].strip()
#       cityToNode[temp1[1].strip()] = temp1[0]
#    fileCities.close()
#
#    fileEdges = open(edges, "r+")
#    for z in fileEdges.readlines():
#       temp2 = z.split(" ")
#       if neighbors.get(temp2[0]) == None:
#          neighbors[temp2[0]] = [temp2[1].strip()]
#       else:
#          neighbors[temp2[0]].append(temp2[1].strip())
#       if neighbors.get(temp2[1]) == None:
#          neighbors[temp2[1].strip()] = [temp2[0]]
#       else:
#          neighbors[temp2[1].strip()].append(temp2[0])
#       y1, x1, y2, x2 = nodeLoc[temp2[0]][0], nodeLoc[temp2[0]][1], nodeLoc[temp2[1].strip()][0], nodeLoc[temp2[1].strip()][1]
#       a = calc_edge_cost(y1, x1, y2, x2)
#       edgeCost[temp2[1].strip(), temp2[0]] = a
#       edgeCost[temp2[0], temp2[1].strip()] = a
#    fileEdges.close()
#
#    for node in nodeLoc: #checks each
#       lat = float(nodeLoc[node][0]) #gets latitude
#       long = float(nodeLoc[node][1]) #gets long
#       modlat = (lat - 10)/60 #scales to 0-1
#       modlong = (long+130)/70 #scales to 0-1
#       map[node] = [modlat*800, modlong*1200] #scales to fit 800 1200
#    info = [nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost, map]
#    sys.setrecursionlimit(10000)
#    pickle.dump(info,open("info.pkl",'wb'))
#
# make_graph()
info = pickle.load(open("info.pkl",'rb'))
nodeLoc, nodeToCity, cityToNode, neighbors, dist, map = info
#id: long,lat|id:cityname|cityname:id|id:neighbors|id1,id2:distance|id:x,y
root = Tk()
root.title("choo choo!")
root.geometry("1200x800")
imagefile = "map2.png"
img = PhotoImage(file=imagefile)
c = Canvas(width=img.width(),height=img.height())
c.pack()
c.pack(fill=BOTH, expand=1) #sets fill expand

for n1, n2 in dist:
    c.
