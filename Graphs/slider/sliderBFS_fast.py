import time
import sys
import math
import random

def neighborsN(board,boardLen,e):# finding neighbors for any size board
    n = []
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

#for 3x3
def n_0(board):
    return ("{}_{}".format(board[1], board[2:]),
        "{}{}_{}".format(board[3] , board[1:3] , board[4:]))
def n_1(board):
    return ("_{}{}".format(board[0], board[2:]),
        "{}{}_{}".format(board[0], board[2], board[3:]),
        "{}{}{}_{}".format(board[0] , board[4] , board[2:4] , board[5:]))

def n_2(board):
    return ("{}_{}{}".format(board[0], board[1], board[3:]),
        "{}{}{}_{}".format(board[:2] , board[5] , board[3:5] , board[6:]))

def n_3(board):
    return ("_{}{}{}".format(board[1:3] , board[0] , board[4:]),
        "{}{}_{}".format(board[:3], board[4], board[5:]),
        "{}{}{}_{}".format(board[:3] , board[6] , board[4:6] , board[7:]))
def n_4(board):
    return ("{}_{}{}{}".format(board[0] , board[2:4] , board[1] , board[5:]),
        "{}_{}{}".format(board[:3], board[3], board[5:]),
            "{}{}_{}".format(board[:4], board[5], board[6:]),
        "{}{}{}_{}".format(board[:4] , board[7] , board[5:7] , board[8]))
def n_5(board):
    return ("{}_{}{}{}".format(board[:2] , board[3:5] , board[2] , board[6:]),
        "{}_{}{}".format(board[:4], board[4], board[6:]),
        "{}{}{}_".format(board[:5] , board[8] , board[6:8]))
def n_6(board):
    return ("{}_{}{}{}".format(board[:3] , board[4:6] , board[3] , board[7:]),
        "{}{}_{}".format(board[:6], board[7], board[8]))
def n_7(board):
    return ("{}_{}{}{}".format(board[:4] , board[5:7] , board[4] , board[8]),
        "{}_{}{}".format(board[:6], board[6], board[8]),
        "{}{}_".format(board[:7], board[8]))
def n_8(board):
    return ("{}_{}{}".format(board[:5] , board[6:8] , board[5]),
        "{}_{}".format(board[:7], board[7]))

def neighbors(board,boardLen, neighbors8):
    e = board.find('_')
    if(boardLen == 3):
        return neighbors8[e](board)
    else:
        return neighborsN(board, boardLen, e)


def impossible(root,goal, width):
    countr,countg = 0,0
    for index, i in enumerate(root):
        if i == "_":
            continue
        for j in range(index+1,len(root)):
            if root[j] !='_' and root[j] < i:
                countr+=1
    for index, i in enumerate(goal):
        if i == "_":
            continue
        for j in range(index+1,len(goal)):
            if goal[j] !='_' and goal[j] < i:
                countg+=1
    if width%2 == 0:
        r = root.find('_') // width
        g = goal.find('_') // width
        countr += abs(r-g)
    return countr %2 != countg %2


def solve(board, goal):
    
    boardLen = int(len(board)**.5 + .5)
    if impossible(board,goal, boardLen):
        return []
    q =[board]
    if board == goal:
        return q
    
    seen = {}
    seen[board] = None
    ptr= 0
    neighbors8 = {0:n_0,
                  1:n_1,
                  2:n_2,
                  3:n_3,
                  4:n_4,
                  5:n_5,
                  6:n_6,
                  7:n_7,
                  8:n_8}
    while q:
        try:
            board = q[ptr] #get next element in the queue but no need to remove it
        except: #no solution because there isnt a new node in q
            return []
        if(board == goal):
            return getPath(board,seen)

        for neighbor in neighbors(board,boardLen,neighbors8):
            if neighbor == goal:
                seen[neighbor] = board
                return getPath(neighbor,seen)
            if neighbor not in seen:
                q.append(neighbor)
                seen[neighbor] = board
        ptr+=1
    return([])


def getPath(board,seen): #build list from goal to start
    path = []
    while(seen[board] is not None):
        path.append(board)
        board = seen[board]
    path.append(start)
    return path[::-1]

def sigRound(x, n):
    return round(x, -1* int(math.log10(x)//1)+n-1)



def printBoards(boards):
    n=12
    boardLen = int(len(boards[0])**.5 + .5)
    batches = [boards[i * n : ( i + 1 ) * n] for i in range((len(boards) + n - 1 ) // n )]
    for batch in batches:
        for layer in range(boardLen):
            print("   ".join([i[layer*boardLen:layer*boardLen+boardLen] for i in batch]))
        print('\n')

start = sys.argv[1]
if len(sys.argv) <3:
    goal = "12345678_"
else:
    goal =sys.argv[2]

pzl = [*'12345678_']
goal  ='12345678_'
t1 = time.time()
lens = []
num_impossible = 0
for _ in range(500):
    random.shuffle(pzl)
    start = ''.join(pzl)
    t_= time.time()
    solution = solve(start,goal)
    #print("Puzzle {0}: {1} => {2} steps \t\t in {3}s".format(_,start,len(solution)-1, round(time.time()-t_,3)))
    if not solution:
        num_impossible+=1
    else:
        lens.append(len(solution))
    if time.time()-t1 >=90:
        break
t2 = time.time()
print("Impossible count: ",num_impossible)
print("Ave len for possibles:", sum(lens)/len(lens))
print("Solved {} puzzles in {}s".format(len(lens),sigRound(t2-t1,3)))


# t1 = time.time()
# solution = solve(start,goal)
# t2 = time.time()

# if solution:
#     printBoards(solution)
#     print(t2-t1)
# else:
#     printBoards([start])

# if(t2-t1 == 0):
#     print('Steps:{0}\nTime: 0 s'.format(len(solution)-1))
# else:
#     print('Steps: {0}\nTime: {1} s'.format(len(solution)-1,sigRound(t2-t1,2)))
