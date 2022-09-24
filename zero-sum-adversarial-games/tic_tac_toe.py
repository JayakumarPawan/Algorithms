import sys
import time
sys.setrecursionlimit(100000)
height = int(sys.argv[2])
width = int(sys.argv[3])
height = min(int(sys.argv[2]),int(sys.argv[3]))
width = max(int(sys.argv[2]),int(sys.argv[3]))
num_win = int(sys.argv[1])
debug = False
if len(sys.argv) >4:
    debug = True
if debug:
    import pdb
    pdb.set_trace()
cache = {} #string board to int num of games from this position
x_wins = set()
o_wins = set()
ties = set()
player = ('o','x')

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
    et = st+(width-1)*(height - min(st//width,width-st%width)-1)
    #print(st,et,move)
    if et < len(board):
        win = board[slice(st,et+1,width-1)]
        #print(st,et,move,win)
        if win.find(num_win*'o') != -1:
            return 1
        if win.find(num_win*'x') != -1:
            return 2

    if board.count('.') == 0:
        #print_board(board)
        #print(f'i {i} ,ix {ix} ,iy {iy},st {st} ,et {et},sd {sd},ed {ed}')
        #exit()
        return 0
    return -1

def print_board(board):
    for i in range(len(board)):
        if i%width ==0 :
            print("")
        print(board[i],end="")
    print("")

def recur(board,turn,index):
    if board in cache.keys():
        return cache[board]
    terminal_state = is_terminal(board,index)

    if terminal_state ==0:
        ties.add(board)
        cache[board] = 1
        return 1
    if terminal_state ==1:
        o_wins.add(board)
        #print_board(board)
        cache[board] = 1
        return 1
    if terminal_state ==2:
        x_wins.add(board)
        cache[board] = 1
        #print_board(board)
        #print(st,et,i,ix,iy)
        return 1

    num_games = 0
    explosion = [*board]
    for index in range(len(board)):
        if board[index] !='.':
            continue
        explosion[index] = player[turn]
        new_board = ''.join(explosion)
        explosion[index] = '.'
        n = recur(new_board,not turn,index)
        cache[new_board] =n
        num_games+=n
    cache[board] = num_games
    return num_games


time1 = time.time()
num_games = recur("."*height*width,True,0)
time1 = time.time() - time1
print(time1)
print("Number of games: {}\nNumber of boards: {}".format(num_games,len(cache.keys())))
print("Number of terminal boards: {}".format(len(x_wins)+len(o_wins)+len(ties)))
print("x wins: {} \no wins: {}".format(len(x_wins),len(o_wins)))
print("ties: {}".format(len(ties)))
