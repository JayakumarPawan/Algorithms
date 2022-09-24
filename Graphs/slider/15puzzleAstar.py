import time
import sys
import math,random

#1605194
#160594
#160594_AB

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

def solve(board, goal):
    boardLen = int(len(board)**.5 + .5)
    if impossible(board,goal,boardLen):
        return 0
    q =[(0,board)]
    buckets = {}
    for i in range(80):
        buckets[i] = set()
    boardLen = int(len(board)**.5 + .5)
    seen = {}
    seen[board] = 0

    while True:
        if(cur != q[-1][1]):
            q.sort(reverse=True)
        board  = q.pop(0)[1]
        if(board == goal):
            return seen[board]
        for neighbor in neighbors(board,boardLen):
            if neighbor == goal:
                return seen[board]+1
            if neighbor not in seen:
                seen[neighbor] = seen[board]+1
                q.append((manhatten(neighbor,goal,boardLen),neighbor))


def getPath(board,seen): #build list from goal to start
    path = []
    while(seen[board] is not None):
        path.append(board)
        board = seen[board]
    #path.append(start)
    return path[::-1]

def sigRound(x, n):
    return round(x, -1* int(math.log10(x)//1)+n-1)


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

def manhatten(board,goal, board_len):
    dist = 0
    for _,i in enumerate(board):
        if i !='_':
            correct = goal.find(i)
            dist+= abs(correct // board_len - _//board_len)
            dist+= abs(_%board_len - correct%board_len)
    return dist

def printBoards(boards):
    n=12
    boardLen = int(len(boards[0])**.5 + .5)
    batches = [boards[i * n : ( i + 1 ) * n] for i in range((len(boards) + n - 1 ) // n )]
    for batch in batches:
        for layer in range(boardLen):
            print("   ".join([i[layer*boardLen:layer*boardLen+boardLen] for i in batch]))
        print('\n')

# start = sys.argv[1]
# if len(sys.argv) <3:
#     goal = "12345678_"
# else:
#     goal =sys.argv[2]
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
    #print("Puzzle {0}: {1} => {2} steps \t\t in {3}s".format(_,start,solution-1, round(time.time()-t_,3)))
    if not solution:
        num_impossible+=1
    else:
        lens.append(solution)
    if time.time()-t1 >=90:
        break
t2 = time.time()
print("Impossible count: ",num_impossible)
print("Ave len for possibles:", sum(lens)/len(lens))
print("Solved {} puzzles in {}s".format(len(lens),sigRound(t2-t1,3)))
