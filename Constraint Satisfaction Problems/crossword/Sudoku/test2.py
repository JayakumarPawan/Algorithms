import sys
import math
import time
import pdb
#pdb.set_trace()
#this version runs between 4 to 5 seconds
def readPuzzle():
    file = "puzzles.txt"
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == 'd':
        debug = True
    if len(sys.argv) > 2 or len(sys.argv) > 1 and debug == False:
        file =sys.argv[1]
    with open(file,'r') as f:
        puzzles = [line.strip() for line in f.readlines()]
    return debug, puzzles

'''
0  1  2  | 3  4  5  | 6  7  8
9  10 11 | 12 13 14 | 15 16 17
18 19 20 | 21 22 23 | 24 25 26

'''
def update(stat,dict):
    if stat in dict:
        dict[stat]+=1
    else:
        dict[stat]=1

def setGlobals():
    debug, puzzles = readPuzzle()
    boardSize = len(puzzles[0])
    boardLen = int(boardSize**.5 + .5)
    blockH = int(boardLen**.5)
    for i in range(blockH,0,-1):
        if(not blockH%boardLen):
            blockH=i
            break
    blockW = boardLen//blockH

    if(boardLen==9):
        SYMSET = {'1','2','3','4','5','6','7','8','9'}
    if(boardLen == 12):
        SYMSET = {'1','2','3','4','5','6','7','8','9','A','B','C'}
    if(boardLen == 16):
        SYMSET = {'1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G'}
    return (debug, boardSize,boardLen,blockW,blockH,SYMSET, puzzles)

def constraintSetGenerator():
    debug, boardSize,boardLen,blockW,blockH,SYMSET, puzzles= setGlobals()
    neighbors = {}
    constraints = []
    '''
    0  1  2  | 3  4  5  | 6  7  8
    9  10 11 | 12 13 14 | 15 16 17
    18 19 20 | 21 22 23 | 24 25 26
    ---------|----------|---------
    27 28 29 | 30 31 32 | 33 34 35
    36 37 38 | 39 40 41 | 42 43 44
    45 56 47 | 48 49 50 | 51 52 53
    ---------|----------|---------
    54 55 56 | 57 58 59 | 60 61 62
    63 64 65 | 66 67 68 | 69 70 71
    72 73 74 | 75 76 77 | 78 79 80
    '''
    # rowStart = {0,9,18,27,36,45,54,63,72}
    # blockStart = {0,3,6,27,30,33,54,57,60}
    # colStart = {0,1,2,3,4,5,6,7,8}
    for i in range(boardSize):
        neighbor = set()
        print(i)

        debug, boardSize,boardLen,blockW,blockH,SYMSET, puzzles= setGlobals()
        neighbors = {}
        constraints = []
        neighbor = set()

        rowStart = i - i%boardLen
        blockStart = i - i%blockW - boardLen*(( i//boardLen)%blockH)
        colStart = i%boardLen
        
        for j in range(boardLen):
            neighbor.add(rowStart+j) #row
            neighbor.add(colStart+j*boardLen) #col

        if i== rowStart:
            row = set()
            for j in range(boardLen):
                row.add(rowStart+j)
            constraints.append(row)

        if i==colStart:
            col = set()
            for j in range(boardLen):
                col.add(colStart+j*boardLen)
            constraints.append(col)

        if i==blockStart:
            block = set()
            for r in range(blockH):
                for c in range(blockW):
                    block.add(blockStart+r*boardLen+c)
            constraints.append(block)

        for r in range(blockH): #block
            for c in range(blockW):
                neighbor.add(blockStart+r*boardLen+c)
                block.add(blockStart+r*boardLen+c)


        neighbors[i] = neighbor
    return (debug, boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints,neighbors)

debug, boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints,neighbors = constraintSetGenerator()
stats = {}


def print_puzzle(pzl):
    for row in range(boardLen):
        if not row %3 and row!=0:
            print("_______|________|________")
        for col in range(boardLen):
            if not col %3 and col!=0:
                print(" | ",end="")
            print(pzl[row*boardLen+col],end=" ")
        print("")

#constraint visualizer
for i in constraints:
    dots = list("."*81)
    print(len(i))
    for index in i:
        dots[index] = "O"
    print_puzzle(dots)
    print("")
print(len(constraints))

stats['findBestSpotTime'] = 0
stats['findOnlySpotsTime'] = 0
stats['wasted'] = 0
stats['2b_lookup'] = 0
def isInvalid(pzl,pos):
    if pos not in neighbors:
        return False
    for index in neighbors[pos]:
        if pzl[index] == '.':
            continue
        if pzl[index] == pzl[pos] and index != pos:
            return True
    return False


def checkSum(solution,boardLen):
    sum =0
    for symbol in solution:
        sum+= ord(symbol)
    sum-= 48*(boardLen**2)
    return sum

def sigRound(x, n):
    return round(x, -1* int(math.log10(x)//1)+n-1)

def invalidOptions(pzl,pos):
    if pzl[pos]!='.':
        return SYMSET
    used = set(pzl[i] for i in neighbors[pos])
    used.discard(".")
    return used

def findBestSpot(pzl,available):
    minOpt = ([0],SYMSET) #2A
    for pos,options in enumerate(available):
        if len(options)==1:
            return ([pos],options)
        if 0 < len(options) < len(minOpt[1]):
            minOpt = ([pos],options)

    for constraint in constraints:#2B
        options = SYMSET - set(pzl[i] for i in constraint)
        for option in options:
            places = set()
            for index in constraint:
                if option in available[index]:
                    places.add(index)
            if len(places) == 1:
                 return (places,[option])
            if len(places) <len(minOpt[1]):
                minOpt = (places,[option])
    return minOpt

def makeDeductions(pzl,available):
    entangled = {} #3a
    for pos,options in enumerate(available):
        if len(options)==2:
            pair = tuple(sorted(options))
            if pair in entangled :

                for pair_index in entangled[pair]:
                    constraint = neighbors[pos]&neighbors[pair_index] #intersection of neighbors
                    constraint.discard(pos)
                    constraint.discard(pair_index)
                    if len(constraint) <7:
                        continue
                    for index in constraint:
                        available[index].discard(pair[0])
                        available[index].discard(pair[1])
                        if(len(available[index])==1):
                            return ([index],available[index])

                entangled[pair].add(pos)
            else:
                entangled[pair]= {pos}
    return('','')

def bruteForce(pzl,pos,available):
    if isInvalid(pzl,pos):
        return ""
    if '.' not in pzl:
        return pzl
    positions,symbols = makeDeductions(pzl,available)
    if not positions:
        positions, symbols  = findBestSpot(pzl,available)
    for pos in positions: #one of these is 1 long
        for symbol in symbols:
            explosion = list(pzl)
            explosion[pos] = symbol
            sub_pzl = "".join(explosion)
            availableNew = [{*j} for j in available] #2c
            availableNew[pos] = set()
            for neighbor in neighbors[pos]:
                availableNew[neighbor].discard(symbol)
            bf = bruteForce(sub_pzl,pos,availableNew)
            if bf:
                return bf
    return ""

totalTime= 0
last =0
if debug:
    pdb.set_trace()
for n,puzzle in enumerate(puzzles):
    t1 = time.time()
    available = [SYMSET - invalidOptions(puzzle,i) for i in range(boardSize)]
    solution = bruteForce(puzzle, 0, available)
    t2 = time.time() - t1
    check = checkSum(solution,boardLen)
    assert check==405 , (print(f'checksum is {check}'),print(solution))
    totalTime+=t2
    last+=1
    print(f"puzzle: {puzzle} \nsolution: {solution}\nPuzzle number: {n+1} checksum: {check} time taken: {totalTime}\n")
print(f"solved {last} in {round(totalTime,3)} seconds")
