import sys
from math import pi , acos , sin , cos, log
import pickle
from tkinter import *
import heapq


nodes = pickle.load(open('nodes.pkl','rb'))
edges = pickle.load(open('edges.pkl','rb'))
info = pickle.load(open("graph.pkl",'rb'))

drawCoords = info[-1]
edgeCost = info[-2]
id_to_name = info[1]
name_to_id = info[2]

class Node:
    def __init__(self,id,lat,long):
        self.id=id
        self.lat=lat
        self.long=long
        self.neighbors={}
        self.name = id_to_name[id] if id in id_to_name.keys() else id
        self.parent = None
        self.depth =0
        self.f = 0
    def __str__(self):
        return self.id
    def __repr__(self):
        return self.__str__()
    def __lt__(self, other):
        return self.f < other.f
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return int(self.long)+int(self.lat)
def calcd(y1,x1, y2,x2):
   #domain error if distance is 0
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degree
   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)
   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   #acos domain from 0 to 180
   try:
       a = acos(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1))* R
       b = acos(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x1-x2))* R
       return min(a,b)
   except:
       return 0

def handleInput(args,name_to_id): #sys.argv
    if len(args) <3:
        return  '3700421', '3200014'
    if len(args) == 3:
        return (name_to_id[args[1]],name_to_id[args[2]])
    if len(args) ==4:
        city1a = args[1]+" "+args[2]
        if(city1a in name_to_id.keys()):
            return name_to_id[city1a],name_to_id[args[3]]

        else:
            city2 = name_to_id[str(args[2]+" "+args[3]).strip()]
            return name_to_id[args[1]], city2

    if len(args) ==5:
        city1 = name_to_id[args[1]+" "+args[2]]
        city2 = name_to_id[args[3]+" "+args[4]]
        return city1, city2


def h(cur, goal):
    return calcd(cur.lat,cur.long,goal.lat,goal.long)

def getPath(start,goal,drawCoords,c, closedSet_lines):
    dist = 0
    path  = []
    cur = start
    while cur.parent:
        path.append(cur)
        cur = cur.parent
    path.append(goal)
    path = path[::-1]
    dist = 0
    print(path[0].id, " distance: ", "0 mi")
    for i in range(1,len(path)):
        c.create_line(drawCoords[path[i].id][1],drawCoords[path[i].id][0], drawCoords[path[i-1].id][1],drawCoords[path[i-1].id][0],fill='purple',width = 3 )
        print(path[i].id , " distance: ", path[i].depth - path[i-1].depth, " mi")
    print("totalDistance: ", start.depth, " mi")
    print("path len: ",len(path)-1)




network = { node1[0]:Node(node1[0], node1[1], node1[2]) for node1 in nodes}

for edge in edges:
    n1 = network[edge[0]].id
    n2 = network[edge[1]].id
    network[edge[0]].neighbors[network[edge[1]]] = edgeCost[n1,n2]
    network[edge[1]].neighbors[network[edge[0]]] = edgeCost[n1,n2]

window = Tk()
window.title("choo choo!")
window.geometry("1200x800")
window.configure(background='black')
c = Canvas(width=1200,height=800, background='black')
c.pack()
c1,c2 = handleInput(sys.argv,name_to_id)
start = network[c1]
goal = network[c2]

for id in network.keys():
    for n in network[id].neighbors:
        c.create_line(drawCoords[id][1],drawCoords[id][0],drawCoords[n.id][1],drawCoords[n.id][0],fill='white')

cc = 0
upd = int(h(start,goal)/5)
openSet_lines = {}
closedSet_lines = {}
openSet =[]
start.f = h(start,goal)
heapq.heappush(openSet, start)
closedSet = set()
while openSet:
    cur = heapq.heappop(openSet)
    if(cur in closedSet):
        continue
    closedSet.add(cur)
    if cur!= start:
        for i in openSet_lines[cur]:
            c.itemconfig(i,fill='green')
        closedSet_lines[cur] = l
    if(cur == goal):
        getPath(cur,start,drawCoords,c,closedSet_lines)
        break
    for n,d in cur.neighbors.items():
        if n in closedSet:
            continue
        if n.depth == 0 or cur.depth+d < n.depth:
            n.parent = cur
            n.depth = cur.depth+d
            n.f = h(n,goal)+n.depth
            heapq.heappush(openSet, n)
            l = c.create_line(drawCoords[cur.id][1],drawCoords[cur.id][0], drawCoords[n.id][1],drawCoords[n.id][0],fill='red',width=2)
            if n in openSet_lines:
                openSet_lines[n].append(l)
            else:
                openSet_lines[n] = [l]
    if cc == upd:
        cc=0
        upd = 100*int(log(len(closedSet)))
        print(upd)
        window.update()
    cc+=1
window.update()
mainloop()
