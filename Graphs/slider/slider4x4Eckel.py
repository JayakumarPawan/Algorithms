import math,sys,time


def neighbor_lookup(boardLen,boardSize):
    ''' 
    this function determines the valid neighbors and the position of a space 
    for each of the possible neighbours of the current board
    '''
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

def neighbors(board,ntable,mtable,gtable):
    '''
    this function creates a list of all the neighbors along with 
    the change in their manhatten distance to the goal
    '''
    n = []
    board = [*board]
    e = board.index('_')
    mdi = mtable[(ntable[e][0], gtable[board[ntable[e][0]]])] #distance from tile to goal before swap
    temp = board[ntable[e][0]] #normal swap
    board[ntable[e][0]] = '_'
    board[e]= temp
    mdn = mtable[ ( e , gtable[ board[e]] )  ] #distance from tile to goal after swap
    dh = mdn - mdi
    n.append(("".join(board), dh))

    for space_pos, index in enumerate(ntable[e][1:]):
        #tripple swap
        mdn = mtable[ ( e , gtable[ board[ntable[e][space_pos+1]]  ] )  ] #distance from tile to goal after swap
        mdi = mtable[(ntable[e][space_pos+1],gtable[ board[ntable[e][space_pos+1]]])] #distance from tile to goal before swap
        dh = mdn - mdi
        board[ntable[e][space_pos]] = board[e]
        board[e] =board[index]
        board[index] = "_"
        n.append(("".join(board),dh))
    return n


def getPath(board,seen): #build list from goal to start
    path = []
    while(seen[board] is not None):
        path.append(board)
        board = seen[board]
    #path.append(start)
    return path[::-1]
def sigRound(x, n):
    return round(x, -1* int(math.log10(x)//1)+n-1)
def goal_lookup(goal):
    dict = {}
    for index, letter in enumerate(goal):
        if letter == '_':
            continue
        dict[letter] = index
    return dict
def manhatten_lookup(boardLen):
    boardSize = boardLen ** 2
    table = {}
    for i in range(boardSize):
        for j in range(boardSize):
            table[(i,j)] = abs(i// boardLen - j//boardLen) + abs(i%boardLen - j % boardLen)
    return table
def manhatten(board,gtable,mtable):
    dist = 0
    for idx, letter in enumerate(board):
        if letter !='_':
            dist+= mtable[(idx,gtable[letter])]
    return dist
def manhattenOLD(board,goal_dict, board_len):
    dist = 0
    for idx, letter in enumerate(board):
        try:
            dist += abs(goal_dict[letter]// board_len - idx//board_len)
            dist+= abs(goal_dict[letter] % board_len - idx % board_len)
        except:
            continue
    return dist
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
def solve(board,goal, gtable, mtable, ntable):
    if goal == board:
        return 0
    boardLen = int(len(board)**.5 + .5)
    if impossible(board,goal,boardLen):
        return -1

    fs = manhatten(board, gtable, mtable)
    closedSet = {}
    openSet = []
    for i in range(fs,100):
        openSet.append([])
    openSet[fs].append((board,0))
    for f , boards in enumerate(openSet):
        if not boards:
            continue
        while boards:
            board,depth = boards.pop()
            if board in closedSet:
                continue
            closedSet[board] = depth
            for neighbor,dh in neighbors(board,ntable,mtable,gtable):
                if neighbor == goal:
                    return closedSet[board]+1
                if neighbor not in closedSet and (neighbor,dh) not in openSet:
                    fn = f+1+dh
                    openSet[fn].append((neighbor,depth+1))

f = sys.argv[1] if len(sys.argv) > 1 else "eckel.txt"
with open(f,'r') as f:
    s = f.read()
    puzzles = [s[i:i+16] for i in range(0,len(s),17)]
    t1 = time.time()
    lens = []
    num_impossible = 0
    goal = puzzles[0]
    boardLen = int(len(goal)**.5 + .5)
    gtable  = goal_lookup(goal)
    mtable = manhatten_lookup(boardLen)
    ntable = neighbor_lookup(boardLen, len(goal))
    for num, start in enumerate(puzzles):
        t_= time.time()
        if num == 0:
            goal  = start
        solution = solve(start,goal,gtable,mtable,ntable)
        if time.time()-t1 >=120:
            break
        if solution == -1:
            num_impossible+=1
        else:
            lens.append(solution)

        print("Puzzle {0}: {1} => {2} steps \t\t in {3}s".format(num,start,solution, round(time.time()-t_,3)))
    t2 = time.time()
    print("Impossible count: ",num_impossible)
    print("Ave len for possibles:", sum(lens)/len(lens))
    print("Solved {} puzzles in {}s".format(len(lens)-1,sigRound(t2-t1,3)))
