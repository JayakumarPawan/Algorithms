import sys
import pdb
num_win = int(sys.argv[1])
height = int(sys.argv[2])
width = int(sys.argv[3])
debug = int(sys.argv[4])
if debug:
    pdb.set_trace()
game_tree = {} #string representing game move sequence: board this sequence leads to
board_space= set() # set of all possible boards
game_space = set()
x_wins = set() #set of all possible boards where x wins
o_wins = set() #set of all possible boards where o wins
ties = set() #set of all possible terminal boards where nobody wins
def diag(i):
    ix = i%width
    iy = i//width
    limit = min(width-ix,height-iy)

def is_terminal(board,i):
    ix = i%width
    iy = i//width

    sr = i-ix
    er = i+ width-ix
    win = board[sr:er]
    if win.find(num_win*'o') != -1:
        return 1
    if win.find(num_win*'x') != -1:
        return 2

    sc = ix
    ec = len(board)-width+ix
    win = board[slice(sc,ec+1,width)]
    if win.find(num_win*'o') != -1:
        return 1
    if win.find(num_win*'x') != -1:
        return 2

    sd = (iy - min(ix,iy))*width + ix-min(ix,iy) #\
    ed = sd+(width+1)*(height - max(sd//width,sd%width)-1)
    #print(sd,ed)
    if ed < len(board):
        win = board[slice(sd,ed+1,width+1)]
        if win.find(num_win*'o') != -1:
            return 1
        if win.find(num_win*'x') != -1:
            return 2
    move = min(iy, width-1-ix)
    st = (iy - move)*width + ix+move #/
    et = st+(width-1)*(height - st//width-1)
    #print(st,et,move)
    if et < len(board):
        win = board[slice(st,et+1,width-1)]
        #print(st,et,move,win)
        if win.find(num_win*'o') != -1:
            return 1
        if win.find(num_win*'x') != -1:
            return 2

    if board.count('.') == 0:
        print_board(board)
        print(f'i {i} ,ix {ix} ,iy {iy},st {st} ,et {et},sd {sd},ed {ed}, sdx {sd%width} sdy {sd//width}')
        #exit()
        return 0
    return -1

'''
0 1 2 3
4 5 6 7
8 9 A B
'''
def print_board(board):
    for i in range(len(board)):
        if i%width ==0 :
            print("")
        print(board[i],end="")
    print("")
board = 'xooxoxxoxooxxoxo'
print_board(board)
print(is_terminal(board,10)) #lr
