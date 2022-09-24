import sys,re
#import pdb; pdb.set_trace()

blocks = (lambda b=re.split('[xX ]', ' '.join(sys.argv[1:])): [(int(b[i]), int(b[i+1])) for i in range(0, len(b), 2)])()
container = blocks.pop(0)
height = container[0]
width = container[1]
area_container = height*width
area_rects= sum([i[0]*i[1] for i in blocks])

def print_puzzle(board):
    for h in range(height):
        for w in range(width):
            print(board[h*width+w],end="")
        print("")
    print("")

def doesNotOverlap(board,block,pos):
    if max(block[0],block[1]) > max(height,width):
        print("no solution")
        exit()
    if (pos%width+block[1] > width or pos//width + block[0] > height):
        return False
    for i in range(block[1]):
        if board[pos+i] !='.':
            return False
        if board[pos+(block[0]-1)*width+i] !='.':
            return False
    for i in range(block[0]):
        if board[pos+width*i] !='.':
            return False
        if board[pos+i*width+block[1]-1] !='.':
            return False
    return True

def solve(board,blocks):
    if len(blocks)==0:
        print(placed)
        if '.' in board:
            for i in range(board.index('.'),len(board)):
                if board[i]=='.':
                    placed.append((1,1))
        print_puzzle(board)
        return placed
    if '.' not in board and blocks:
        return("")
    tries = tryThese(board,blocks)
    for try in tries:
        bf = solve(try,blocks)
        if bf:
            return bf
        
def bruteForce(board,blocks,placed): #placed is decomposition
    if len(blocks)==0:
        print(placed)
        if '.' in board:
            for i in range(board.index('.'),len(board)):
                if board[i]=='.':
                    placed.append((1,1))
        print_puzzle(board)
        return placed
    if '.' not in board and blocks:
        return("")
    pos = board.index('.')
    for i in range(len(blocks)):
        block = blocks[i]
        if doesNotOverlap(board,block,pos):
            sub_board = board[:]
            for row in range(block[0]):
                for col in range(block[1]):
                    sub_board[width*(row+pos//width) + col+pos%width] = chr(65+len(blocks))
            placed.append(blocks.pop(i))
            #print_puzzle(board)
            #print(blocks)
            bf = bruteForce(sub_board,blocks,placed)
            if bf:
                return bf
            else:
                placed.pop()
                blocks.insert(i,block)
        #try rotating
        rotated = (block[1],block[0])
        if block[0] != block[1] and doesNotOverlap(board,rotated,pos):
            sub_board = board[:]
            for row in range(rotated[0]):
                for col in range(rotated[1]):
                    sub_board[width*(row+pos//width) + col+pos%width] = chr(65+len(blocks))
            placed.append(rotated)
            blocks.pop(i)
            #print_puzzle(board)
            #print(blocks)
            bf = bruteForce(sub_board,blocks,placed)
            if bf:
                return bf
            else:
                placed.pop()
                blocks.insert(i,block)
    placed.append((1,1))
    sub_board = board[:]
    sub_board[pos]='_'
    bf = bruteForce(sub_board,blocks,placed)
    if bf:
        return bf
    else:
        placed.pop()



if area_rects > area_container:
    print("No solution")
else:
    board = list('.'*(height*width))
    blocks = sorted(blocks,key= lambda area: (-1*area[0]*area[1]) ) #sort blocks based on area from large to small
    solution =bruteForce(board,blocks,[])
    #print_puzzle(board)
    if solution:
        print("Decomposition: ",solution)
    else:
        print("no solution")
