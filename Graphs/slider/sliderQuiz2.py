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

def getDist(board):
    q =[board]
    boardLen = int(len(board)**.5 + .5)
    seen = {}
    ld = {}
    seen[board] = (None,0)
    for board in q:
        try:
            ld[seen[board][1]+1] +=1
        except:
            ld[seen[board][1]+1] = 1
        for neighbor in neighbors(board,boardLen):
            if neighbor not in seen:
                q.append(neighbor)
                seen[neighbor] = (board,seen[board][1]+1)
                if(seen[board][1]+1 ==24):
                    print(neighbor)
                    exit()
    return seen,ld


def getPath(board,seen): #build list from goal to start
    path = []
    while(seen[board] is not None):
        path.append(board)
        board = seen[board]
    path.append(start)
    return path[::-1]

start = '1234_5678'

graph, lvlDist = getDist(start)
lvls = [i for i in lvlDist.keys()]
maxLevel = sorted(lvls)[25  ]
print(maxLevel-1)
print(lvlDist[24])
