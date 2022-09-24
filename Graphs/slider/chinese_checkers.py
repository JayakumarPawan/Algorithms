import pdb
import sys
#neighbors, board properties, terminating conditions
#move notation: peg being jumped over and direction: / \ -

BS = "\\" #back slash

valid_moves = {
    0: [(1,3,'/'),(2,5,BS)], #peg it can jump over, hole it lands into, direction
    1: [(3,6,'/'),(4,8,BS)],
    2: [(4,7,'/'),(5,9,BS)],
    3: [(1,0,'/'),(6,10,'/'),(4,5,'-'),(7,12,BS)],
    4: [(7,11,'/'),(8,13,BS)],
    5: [(2,0,BS),(9,14,BS),(8,12,'/'),(4,3,'-')],
    6: [(3,1,BS),(7,8,'-')],
    7: [(4,2,'/'),(8,9,'-')],
    8: [(4,1,BS),(7,6,'-')],
    9: [(5,2,BS),(8,7,'-')],
    10:[(6,3,'/'),(11,12,'-')],
    11:[(7,4,'/'),(12,13,'-')],
    12:[(7,3,BS),(8,5,'/'),(13,14,'-'),(11,10,'-')],
    13:[(8,4,BS),(12,11,'-')],
    14:[(5,9,BS),(13,12,'-')]}

def neighbors(pzl):
    ns = [] #neighbors
    for pos,moves in valid_moves.items():
        if pzl[pos]=='.':
            continue
        for move in moves:
            if(pzl[move[0]]=='1' and pzl[move[1]]=='.'):
                #print(pos,move)
                ns.append([pos,move])
    return ns

def process_move(pzl,move):#updates the state of the board after applying a move
    start = move[0]
    mid = move[1][0]
    end = move[1][1]
    move = str(move[1][0])+move[1][2]
    explosion = [*pzl]
    explosion[start] ='.'
    explosion[mid] = '.'
    explosion[end] = '1'
    ret = "".join(explosion)
    return ret,move


def atGoalA(pzl,startingPos):
    if pzl[startingPos] =='1' and pzl.count(".")==14:
        return True
    return False

def atGoalB(pzl,startingPos):
    if pzl[startingPos]=='.' and pzl.count(".")==14 and pzl.count("1")==1: #just to make sure pzl didnt get corrupted
        return True
    return False

def pathToMoves(graph):
    return moves

'''
-----0----
----1-2---
---3-4-5--
--6-7-8-9-
-A-B-C-D-E

pzlprint = ' '.join(list(pzl))
for i in range 4:
    print(i*' ',)
'''
def print_board(pzl):
    print("     "," ".join(list(pzl[0])))
    print("    "," ".join(list(pzl[1:3])))
    print("   "," ".join(list(pzl[3:6])))
    print("  "," ".join(list(pzl[6:10])))
    print(" "," ".join(list(pzl[10:])))

# #test neighbors function
# start = "1.1.11111111111"
# print_board(start)
# ns = neighbors(start)
# assert ns,"no neighbors"
# for n in ns:
#     board,move = process_move(start,n)
#     print_board(board)
#     print(f"move: {move}\n")
# #test goals:
# print(atGoalB('1..............',0))
start = "1.1.11111111111"
if len(sys.argv) > 1:
    start = sys.argv[1]

def solve(pzl):
    startingPos = pzl.find(".")
    q = [pzl]
    seen = {}
    seen[pzl] = ('','')
    for pzl in q:
        print_board(pzl)
        #pdb.set_trace()
        if atGoalA(pzl,startingPos):
            print("pzl",pzl)
            return seen
        ns = neighbors(start)
        print('neighbors of puzzle above:')
        for n in ns:
            board,move = process_move(pzl,n)
            if board in seen:
                continue
            print_board(board)
            q.append(board)
            seen[board] = (pzl, move)
        print("-----------------------")

seen = solve(start)
