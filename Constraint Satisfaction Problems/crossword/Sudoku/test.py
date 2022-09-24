def setGlobals():
    puzzle = ".41....3.6....91.23......6........2...........7........2......71.86....9.9....85."
    boardSize = 81
    boardLen = 9
    SYMSET = {'1','2','3','4','5','6','7','8','9'}
    return (boardSize,boardLen,SYMSET, puzzle)

blocks = [ {0,1,2,3,4,9,10,18,27}, #yellow
           {5,6,7,8,16,17,26,35,44}, #red
           {11,12,13,14,19,20, 23,32,33}, #orange
           {15,24,25,34,43,52,51,50,59},#Lime
           {21,28,29,30,37,46,55,56,65}, #pink
           {22,31,38,39,40,41,42,49,58}, #purple
           {36,45,54,63,72,64,73,74,75}, #grey
           {47,48,57,66,67,68,69,60,61}, #green
           {53,62,70,71,76,77,78,79,80}] # blue

def constraintSetGenerator():
    boardSize,boardLen,SYMSET, puzzle= setGlobals()
    neighbors = {}
    constraints = []
    for i in range(boardSize):
        neighbor = set()
        for block in blocks:
            if i in block:
                neighbor|=block
        row = set()
        col = set()
        rowStart = i - i%boardLen
        colStart = i%boardLen

        for j in range(boardLen):
            neighbor.add(rowStart+j) #row
            row.add(rowStart+j)
            neighbor.add(colStart+j*boardLen) #col
            col.add(colStart+j*boardLen)

        if row not in constraints:
            constraints.append(row)
        if col not in constraints:
            constraints.append(col)

        neighbors[i] = neighbor
    for i in blocks:
        constraints.append(i)


    return (boardSize,boardLen,SYMSET,puzzle,constraints,neighbors)

boardSize,boardLen,SYMSET,puzzle,constraints,neighbors = constraintSetGenerator()


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
    used = set()
    for index in neighbors[pos]:
        used.add(pzl[index])
    used.discard(".")
    return used

def findBestSpot(pzl):
    minOpt = (0,SYMSET)
    avaliable ={}
    for pos,sym in enumerate(pzl):
        if sym != '.':
            continue
        options = SYMSET - invalidOptions(pzl,pos)
        avaliable[pos] = options
        # if len(options) ==1:
        #     return (pos,options,0)
        if len(options) and len(options) < len(minOpt[1]):
            minOpt = (pos,options)
    #for constraint in constraints:
    #   has to go = f(constraint)
    #   for pos in constraint:
    #       check if has to go is in avaliable
    #           if it is, put it in, else go next
    minOpt2  = (1,constraints[0]) #to keep track of whether its 2a or 2b
    for constraint in constraints:
        used = set(pzl[i] for i in constraint)
        options = SYMSET - used
        for option in options:
            places = set()
            for index in constraint:
                if pzl[index] !='.':
                    continue
                if option in avaliable[index]:
                    places.add(index)
            if len(places) == 1:
                return (option,places,1)
            if len(places) <len(minOpt2[1]):
                minOpt2 = (option,places)
    if len(minOpt[1]) < len(minOpt2[1]):
        return (minOpt[0],minOpt[1],0)
    else:
        return (minOpt2[0],minOpt2[1],1)

def bruteForce(pzl,pos):
    if isInvalid(pzl,pos):
        return ""
    if '.' not in pzl:
        return pzl
    single, iter, option  = findBestSpot(pzl) #0 = 2a 1 = 2b iter is places or symbols to iter over single is  symbol or pos

    for i in iter: #either symbol or position
        explosion = list(pzl)
        if option==0:
            explosion[single] = i #symbol
            sub_pzl = "".join(explosion)
            bf = bruteForce(sub_pzl,single)
            if bf:
                return bf
        else:
            explosion[i] = single#position
            sub_pzl = "".join(explosion)
            bf = bruteForce(sub_pzl,i)
            if bf:
                return bf
    return ""



solution = bruteForce(puzzle, 0)
print(solution)
check = checkSum(solution,boardLen)
assert check==405 , (print(f'checksum is {check}'),print(solution))
