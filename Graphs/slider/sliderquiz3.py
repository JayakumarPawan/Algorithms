import pdb
def neighbors(board,boardLen):# finding neighbors for any size board
    n = []
    e = board.find("_")
    emod = e %boardLen
    if(e+boardLen < len(board)):
        n.append("{}{}{}_{}".format(board[:e] , board[e+boardLen] , board[e+1:e+boardLen] , board[e+boardLen+1:])) #down
    if(emod != boardLen-1): #right
        n.append("{}{}_{}".format(board[:e], board[e+1], board[e+2:]))
    if(e >= boardLen):
        n.append( "{}_{}{}{}".format(board[:e-boardLen] , board[e-boardLen+1:e] , board[e-boardLen] , board[e+1:])) # up
    if emod: #left
        n.append( "{}_{}{}".format(board[:e-1], board[e-1], board[e+1:]))
    return n

def solve(board,ntable):
    q =[board]
    boardLen = int(len(board)**.5 + .5)
    seen = {}
    seen[board] = (0,0) #depth/ placeholder
    leaves = set()
    for board in q:
        count =0
        for neighbor in neighbors(board,boardLen):
            if neighbor not in seen:
                count+=1
                q.append(neighbor)
                seen[neighbor] = (seen[board][0]+1,0)
        if count==0:
            leaves.add(board)
    return leaves, seen


def neighbor_lookup(boardLen,boardSize):
    dict  ={}
    for i in range(boardSize):
        dict[i] = []
        if(i+boardLen < boardSize):
            dict[i].append(i+boardLen)
        if(i >=boardLen):
            dict[i].append(i-boardLen)
        if(i % boardLen != 0):
            dict[i].append(i-1)
        if(i % boardLen != boardLen-1):
            dict[i].append(i+1)
    return dict

def getPath(board,seen): #build list from goal to start
    path = []
    while(seen[board] is not None):
        path.append(board)
        board = seen[board]
    path.append(start)
    return path[::-1]

ntable = neighbor_lookup(3,9)

leaves, graph = solve("12345678_",ntable)
print(len(leaves))
dist = {}
for i in range(32):
    dist[i] = 0
for leaf in leaves:
    depth = graph[leaf][0]
    dist[depth]+=1

print(dist)
