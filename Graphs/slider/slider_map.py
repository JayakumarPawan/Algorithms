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

def solve(board,goal):
    q =[board]
    boardLen = int(len(board)**.5 + .5)
    seen = {}
    seen[board] = (None,0)
    if board == goal:
        print( seen[board][1])
        return seen
    for board in q:
        for neighbor in neighbors(board,boardLen):
            if neighbor not in seen:
                q.append(neighbor)
                seen[neighbor] = (board,seen[board][1]+1)
    return seen


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

def getPath(board,seen): #path found
    while(seen[board] is not None):
        path.append(board)
        board = seen[board]
    path.append(start)
    return path[::-1]

def isvalid1(board, ntable): #no two neighbor tiles differ by exactly 1
    for index, number  in enumerate(board):
        adjacents = ntable[index]
        for adj in adjacents:
            try:
                if abs(int(board[adj]) - int(number)) == 1:
                    return False
            except:
                continue
    return True
def isvalid2(board1, board2): # every tile in a different position
    for i in range(len(board1)):
        if board1[i] == board2[i]:
            return False
    return True

def isvalid4(board): #no space in middle
    return board[4] != "_"

ntable = neighbor_lookup(3,9)

graph =solve("1234567_8","84765231_")
