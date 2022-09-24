import sys
import math
import time
import pdb
sys.setrecursionlimit(10**6)
def readPuzzle():
    file = "puzzles.txt"
    if len(sys.argv) > 1:
        file =sys.argv[1]

    with open(file,'r') as f:
        puzzles = [line.strip() for line in f.readlines()]
    return puzzles

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
    puzzles = readPuzzle()
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
    return (boardSize,boardLen,blockW,blockH,SYMSET, puzzles)

def constraintSetGenerator():
    boardSize,boardLen,blockW,blockH,SYMSET, puzzles= setGlobals()
    neighbors = {}
    constraints = []
    for i in range(boardSize):
        neighbor = set()
        row = set()
        col = set()
        block = set()
        rowStart = i - i%boardLen
        blockStart = i - i%blockW - boardLen*(( i//boardLen)%blockH)
        colStart = i%boardLen
        for j in range(boardLen):
            neighbor.add(rowStart+j) #row
            row.add(rowStart+j)
            neighbor.add(colStart+j*boardLen) #col
            col.add(colStart+j*boardLen)
        for r in range(blockH): #block
            for c in range(blockW):
                neighbor.add(blockStart+r*boardLen+c)
                block.add(blockStart+r*boardLen+c)
        constraints.append(row)
        constraints.append(col)
        constraints.append(block)
        neighbors[i] = neighbor
    return (boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints,neighbors)

boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints,neighbors = constraintSetGenerator()
avaliable = [SYMSET for i in range(boardSize)]
stats = {}
stats['invalidTime'] = 0
stats['findBestSpotTime'] = 0
stats['findOnlySpotsTime'] = 0
def isInvalid(pzl,pos):
    if pos not in neighbors:
        return False
    for index in neighbors[pos]:
        if pzl[index] == '.':
            continue
        if pzl[index] == pzl[pos] and index != pos:
            return True
    return False

def print_puzzle(pzl):
    for row in range(boardLen):
        if not row %3 and row!=0:
            print("_______|________|________")
        for col in range(boardLen):
            if not col %3 and col!=0:
                print(" | ",end="")
            print(pzl[row*boardLen+col],end=" ")
        print("")

def checkSum(solution,boardLen):
    sum =0
    for symbol in solution:
        sum+= ord(symbol)
    sum-= 48*(boardLen**2)
    return sum



def sigRound(x, n):
    return round(x, -1* int(math.log10(x)//1)+n-1)

def invalidOptions(pzl,pos):
    used = set()
    for index in neighbors[pos]:
        used.add(pzl[index])
    used.discard(".")
    return used

def findBestSpot(pzl):
    minOpt = (0,SYMSET)
    for pos,sym in enumerate(pzl):
        if sym != '.':
            continue
        options = SYMSET - invalidOptions(pzl,pos)
        if len(options) ==1:
            return (pos,options)
        if len(options) and len(options) < len(minOpt[1]):
            minOpt = (pos,options)

    return minOpt

def findOnlySpots(pzl):
    #minOpt  = ('0',set(range(9)))
    minOpt = (0,SYMSET)
    for constraint in constraints:
        used = set(pzl[i] for i in constraint)
        options = SYMSET-used
        for option in options:
            places = set()
            for index in constraint:
                if pzl[index] !='.':
                    continue
                used = set(pzl[i] for i in neighbors[index])
                if option not in used:
                    places.add(index)
            if len(places) == 1:
                return (option,places)
            if len(places) <len(minOpt[1]):
                minOpt = (option,places)
    return minOpt


def bruteForce(pzl,pos):
    if isInvalid(pzl,pos):
        return ""
    if '.' not in pzl:
        return pzl
    placePos, options = findBestSpot(pzl)
    if len(options)==1:
        explosion = list(pzl)
        explosion[placePos] = options.pop()
        sub_pzl = "".join(explosion)
        bf = bruteForce(sub_pzl,placePos)
        if bf:
            return bf
    sym, places = findOnlySpots(pzl)
    if len(places) < len(options):
        for place in places:
            explosion = list(pzl)
            explosion[place] = sym
            sub_pzl = "".join(explosion)
            bf = bruteForce(sub_pzl,placePos)
            if bf:
                return bf
    else:
        for sym in options:
            explosion = list(pzl)
            explosion[placePos] = sym
            sub_pzl = "".join(explosion)
            bf = bruteForce(sub_pzl,placePos)
            if bf:
                return bf
    return ""

# constraint visualizer
# for i in neighbors.values():
#     dots = list("."*81)
#     for index in i:
#         dots[index] = "O"
#     print_puzzle(dots)
#     print("")
# #
totalTime= 0
last =0
for n,puzzle in enumerate(puzzles):
    t1 = time.time()
    solution = bruteForce(puzzle,0)
    t2 = time.time() - t1
    check = checkSum(solution,boardLen)
    assert check==405 , (print(f'checksum is {check}'),print(solution))
    totalTime+=t2
    last+=1
    print(f"puzzle: {puzzle} \nsolution: {solution}\nPuzzle number: {n} checksum: {check} time taken: {totalTime}\n")
print(f"solved {last} in {round(totalTime,3)} seconds")
