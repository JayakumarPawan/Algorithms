import sys,re,time
#import pdb; pdb.set_trace()

blocks = (lambda b=re.split('[xX ]', ' '.join(sys.argv[1:])): [(int(b[i]), int(b[i+1])) for i in range(0, len(b), 2)])()
container = blocks.pop(0)
height = container[0]
width = container[1]
area_container = height*width
area_rects= sum([i[0]*i[1] for i in blocks])
if area_rects > area_container:
    print("No solution")
    exit()
impossible_even = True
all_squares = True
for block in blocks:
    if block[0] %2!=0 or block[1]%2!=0:
        impossible_even = False
    if block[0] != block[1]:
        all_squares = False
    if max(block[0],block[1]) > max(height,width):
        print("no solution")
        exit()
if all_squares:
    print("oof")
    exit()
if impossible_even and (height %2 != width%2) and area_rects == area_container:
    print('no solution')
    exit()
if len(blocks)==1:
    if max(blocks[0][0],blocks[0][1]) == max(height,width) and min(blocks[0][0],blocks[0][1]) == min(height,width):
        print("Decomposition: ({},{})".format(height,width))
        exit()
time_check = 0
def print_puzzle(board):
    for h in range(height):
        for w in range(width):
            print(board[h*width+w],end="")
        print("")
    print("")

def doesNotOverlap(board,block,pos):
    if (pos%width+block[1] > width or pos//width + block[0] > height):
        return False
    for i in range(block[1]):
        if board[pos+i] !='.':
            return False
        # if board[pos+(block[0]-1)*width+i] !='.':
        #     return False
    for i in range(block[0]):
        # if board[pos+width*i] !='.':
        #     return False
        if board[pos+i*width+block[1]-1] !='.':
            return False
    return True

def bruteForce(board,blocks,placed): #placed is decomposition
    '''
    speedups?:
    keep track of unvisited using a variable
    '''
    #print("".join(board))
    if len(blocks)==0:
        print(placed)
        if '.' in board:
            if sum([i[0]*i[1] for i in placed]) == area_rects:
                return placed
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
        if block[0]==block[1]:
            continue
        rotated = (block[1],block[0])
        if doesNotOverlap(board,rotated,pos):
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
    if area_rects == area_container: #no hole
        return("")
    placed.append((1,1))
    sub_board = board[:]
    sub_board[pos]='_'
    bf = bruteForce(sub_board,blocks,placed)
    if bf:
        return bf
    else:
        placed.pop()




board = list('.'*(height*width))
blocks = sorted(blocks,key= lambda area: (-1*area[0]*area[1]) ) #sort blocks based on area from large to small
solution =bruteForce(board,blocks,[])
#print_puzzle(board)
if solution:
    print("Decomposition: ",solution)
else:
    print("no solution")
