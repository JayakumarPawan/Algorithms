import sys
import math
import time
import pdb
#pdb.set_trace()
sys.setrecursionlimit(10**6)
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
    return (debug, boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints,neighbors)

debug, boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints,neighbors = constraintSetGenerator()
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

def findBestSpot(pzl,available):
    minOpt = (0,SYMSET)
    for pos,sym in enumerate(pzl):
        if sym != '.':
            continue
        options = available[pos]
        if len(options) ==1:
            return (pos,options,0)
        if len(options) and len(options) < len(minOpt[1]):
            minOpt = (pos,options)

    minOpt2  = (1,constraints[0]) #to keep track of whether its 2a or 2b
    for constraint in constraints:
        used = set(pzl[i] for i in constraint)
        options = SYMSET - used
        for option in options:
            places = set()
            for index in constraint:
                if pzl[index] !='.':
                    continue
                if option in available[index]:
                    places.add(index)
            if len(places) == 1:
                return (option,places,1)
            if len(places) <len(minOpt2[1]):
                minOpt2 = (option,places)

    if len(minOpt[1]) < len(minOpt2[1]):
        return (minOpt[0],minOpt[1],0)
    else:
        return (minOpt2[0],minOpt2[1],1)

def bruteForce(pzl,pos,available):
    if isInvalid(pzl,pos):
        return ""
    if '.' not in pzl:
        return pzl
    t1 = time.time()
    single, iter, option  = findBestSpot(pzl,available) #0 = 2a 1 = 2b iter is places or symbols to iter over single is  symbol or pos
    stats['findOnlySpotsTime']+= time.time()- t1
    for i in iter: #either symbol or position
        explosion = list(pzl)
        if option==0:
            explosion[single] = i #symbol
            sub_pzl = "".join(explosion)
            availableNew = [{k for k in j} for j in available]
            for neighbor in neighbors[single]:
                availableNew[neighbor] -= invalidOptions(pzl, neighbor)
                #availableNew[neighbor].discard(i)
            bf = bruteForce(sub_pzl,single,available)
            if bf:
                return bf
        else:
            explosion[i] = single#position
            sub_pzl = "".join(explosion)
            availableNew = [{i for i in j} for j in available]
            for neighbor in neighbors[i]:
                availableNew[neighbor]-= invalidOptions(pzl, neighbor)
                #available[neighbor].discard(single)
            bf = bruteForce(sub_pzl,i,available)
            if bf:
                return bf
    return ""

totalTime= 0
last =0
if debug:
    pdb.set_trace()
for n,puzzle in enumerate(puzzles[:52]):
    t1 = time.time()
    available = [SYMSET - invalidOptions(puzzle,i) for i in range(boardSize)]
    solution = bruteForce(puzzle, 0, available)
    t2 = time.time() - t1
    check = checkSum(solution,boardLen)
    assert check==405 , (print(f'checksum is {check}'),print(solution))
    totalTime+=t2
    last+=1
    print(f"puzzle: {puzzle} \nsolution: {solution}\nPuzzle number: {n} checksum: {check} time taken: {totalTime}\n")
print(f"solved {last} in {round(totalTime,3)} seconds")

print("\n".join([f'{key}:{value}' for key, value in stats.items()]))
