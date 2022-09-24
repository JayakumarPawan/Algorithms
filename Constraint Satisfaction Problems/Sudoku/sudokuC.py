import sys
import math
import time
import pdb
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
    for i in range(boardSize):
        neighbors = set()
        rowStart = i - i%boardLen
        blockStart = i - i%blockW - boardLen*(( i//boardLen)%blockH)
        colStart = i%boardLen
        for j in range(boardLen):
            neighbors.add(rowStart+j) #row
            neighbors.add(colStart+j*boardLen) #col
        for r in range(blockH): #block
            for c in range(blockW):
                neighbors.add(blockStart+r*boardLen+c)
        constraints[i] = neighbors
    return (boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints)

boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints = constraintSetGenerator()

def isInvalid(pzl,pos,constraints):
    #pdb.set_trace()
    if pos not in constraints:
        return False
    # print(sym,constraints[i])
    for index in constraints[pos]:
        # print("\t",pzl[index])
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

def bruteForce(pzl,pos):
    if isInvalid(pzl,pos-1,constraints):
        return ""
    if pos == boardSize:
        return pzl
    if pzl[pos] !='.':
        return bruteForce(pzl,pos+1) #they put one for us
    for sym in SYMSET:
        explosion = list(pzl)
        explosion[pos] = sym
        sub_pzl = "".join(explosion)
        # print(sub_pzl)
        bf = bruteForce(sub_pzl,pos+1)
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
for n,puzzle in enumerate(puzzles   ):
    t1 = time.time()
    solution = bruteForce(puzzle,0)
    t2 = time.time() - t1
    check = checkSum(solution,boardLen)
    assert check==405 , (print(f'checksum is {check}'),print_puzzle(solution))
    totalTime+=t2
    if totalTime > 120:
        last = n
        break
    print(f"puzzle: {puzzle} \nsolution: {solution}\nPuzzle number: {n} checksum: {check} time taken: {totalTime}\n")
print(f"solved {last} in {round(totalTime,3)} seconds")

#dies at pzl 51, does first 50 in 20 seconds
