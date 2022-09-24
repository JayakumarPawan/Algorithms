import sys


def readPuzzle():
    file = "puzzles.txt"
    debug = False
    if len(sys.argv) > 1:
        file =sys.argv[1]
    with open(file,'r') as f:
        puzzles = [line.strip() for line in f.readlines()]
    return puzzles
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
        if row not in constraints:
            constraints.append(row)
        if col not in constraints:
            constraints.append(col)
        if block not in constraints:
            constraints.append(block)
        neighbors[i] = neighbor
    return (boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints,neighbors)

boardSize,boardLen,blockW,blockH,SYMSET,puzzles,constraints,neighbors = constraintSetGenerator()

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
def invalidOptions(pzl,pos):
    if pzl[pos]!='.':
        return SYMSET
    used = set(pzl[i] for i in neighbors[pos])
    used.discard(".")
    return used
def findBestSpot(pzl,available):
    entangled = {}
    minOpt = ([0],SYMSET) #2A
    for pos,options in enumerate(available):
        if len(options)==1:
            return ([pos],options)
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
def bruteForce(pzl,pos,available):
    if isInvalid(pzl,pos):
        return ""
    if '.' not in pzl:
        return pzl
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

#import time
#totalTime= 0
#last =0
for n,puzzle in enumerate(puzzles):
    #t1 = time.time()
    available = [SYMSET - invalidOptions(puzzle,i) for i in range(boardSize)]
    solution = bruteForce(puzzle, 0, available)
    #t2 = time.time() - t1
    check = checkSum(solution,boardLen)
    #assert check==405 , (print(f'checksum is {check}'),print(solution))
    #totalTime+=t2
    #last+=1
    print("{}\n{}\n{}\n{}".format(n+1,puzzle,solution,check))
#     print(f"puzzle: {puzzle} \nsolution: {solution}\nPuzzle number: {n+1} checksum: {check} time taken: {totalTime}\n")
#print(f"solved in {round(totalTime,3)} seconds")
