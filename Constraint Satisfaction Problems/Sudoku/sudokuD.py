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
    constraints = {}
    rows = []
    cols = []
    blocks = []
    for i in range(boardSize):
        neighbors = set()
        row = set()
        col = set()
        block = set()
        rowStart = i - i%boardLen
        blockStart = i - i%blockW - boardLen*(( i//boardLen)%blockH)
        colStart = i%boardLen
        for j in range(boardLen):
            neighbors.add(rowStart+j) #row
            row.add(rowStart+j)
            neighbors.add(colStart+j*boardLen) #col
            col.add(colStart+j*boardLen)
        for r in range(blockH): #block
            for c in range(blockW):
                neighbors.add(blockStart+r*boardLen+c)
                block.add(blockStart+r*boardLen+c)
        rows.append(row)
        cols.append(col)
        blocks.append(block)
        constraints[i] = neighbors
    return (boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints,rows,cols,blocks)

boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints,rows,cols,blocks = constraintSetGenerator()

def isInvalid(pzl,pos):
    if pos not in constraints:
        return False
    for index in constraints[pos]:
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
    for index in constraints[pos]:
        used.add(pzl[index])
    if "." in used:
        used.remove(".")
    return used

def findBestSpot(pzl):
    minOpt = (0,SYMSET)
    for pos,sym in enumerate(pzl):
        if sym == '.':
            options = SYMSET - invalidOptions(pzl,pos)
            if len(options) < len(minOpt[1]):
                minOpt = (pos,options)
            if len(options) ==1:
                return (pos,options)
    return minOpt


def bruteForce(pzl,pos):
    if isInvalid(pzl,pos):
        return ""
    if '.' not in pzl:
        return pzl
    placePos, options = findBestSpot(pzl)
    for sym in options:
        explosion = list(pzl)
        explosion[placePos] = sym
        sub_pzl = "".join(explosion)
        bf = bruteForce(sub_pzl,placePos)
        if bf:
            return bf
    return ""

# constraint visualizer
# for i in constraints.values():
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
