def manhatten(board,goal, board_len):
    dist = 0
    for _,i in enumerate(board):
        if i !='_':
            correct = goal.find(i)
            dist+= abs(correct // board_len - _//board_len)
            dist+= abs(_%board_len - correct%board_len)
    return dist


def neighbor_lookup(boardLen,boardSize):
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

def printBoards(boards):
    n=12
    boardLen = int(len(boards[0])**.5 + .5)
    batches = [boards[i * n : ( i + 1 ) * n] for i in range((len(boards) + n - 1 ) // n )]
    for batch in batches:
        for layer in range(boardLen):
            print("   ".join([i[layer*boardLen:layer*boardLen+boardLen] for i in batch]))
        print('\n')

def neighbors(board,neighbor_indexes):
    n = []
    board = [*board]
    e = board.index('_')
    temp = board[neighbor_indexes[e][0]] #normal swap
    board[neighbor_indexes[e][0]] = '_'
    board[e]= temp
    n.append("".join(board))
    print(neighbor_indexes[e])
    for space_pos, index in enumerate(neighbor_indexes[e][1:]):
        #tripple swap
        board[neighbor_indexes[e][space_pos]] = board[e]
        board[e] =board[index]
        board[index] = "_"
        n.append("".join(board))
    return n
ntable = neighbor_lookup(3, 9)
boards = ["12_345678", "123_45678", "1234_5678"]
for board in boards:
    neighborz = neighbors(board,ntable)
    printBoards([board])
    printBoards(neighborz)
# print(manhatten("82345671_","12345678_",3))


#11:34
#_16059478
