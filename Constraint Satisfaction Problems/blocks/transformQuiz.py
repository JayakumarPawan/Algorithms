import sys
import math
board = sys.argv[1]
boardSize = len(board)
width = int(boardSize**.5 + .5)
while(width < boardSize):
    if (boardSize % width ==0):
        break
    else:
        width+=1

height = boardSize//width
if len(sys.argv) > 2:
    width = int(sys.argv[2])

identity = range(boardSize)
rotate_90ccw = [[i+width*j for j in range(height)]  for i in range(width-1,-1,-1)]
rotate_90cw = [[i+width*j for j in range(height-1,-1,-1)]  for i in range(width)]
rotate_180 = [[boardSize-width*i-j-1 for j in range(width)] for i in range(height)]




ret = []
for i in rotate_90ccw:
    for j in i:
        ret.append(board[j])
ret = ''.join(ret)
print(ret)


ret = []
for i in rotate_90cw:
    for j in i:
        ret.append(board[j])
ret = ''.join(ret)
print(ret)

ret = []
for i in rotate_180:
    for j in i:
        ret.append(board[j])
ret = ''.join(ret)
print(ret)

print(board)
