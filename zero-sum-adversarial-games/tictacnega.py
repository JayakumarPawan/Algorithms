import sys

board = sys.argv[1]
other = {'x': 'o', 'o': 'x'}
if len(sys.argv) > 2:
    width = sys.argv[3]

height = int(len(board) ** .5)
for i in range(height, 0, -1):
    if (not height % len(board)):
        height = i
        break
width = len(board) // height

num_win = 3

def parseCons(cons, wLen):
  if len(cons) < wLen: return
  if len(cons) > wLen:
    for i in range(len(cons)):
      if i + wLen <= len(cons):
        look.append(set(cons[i:i + wLen]))
  else:
    look.append(set(cons))


def makeLookup(w, size, wLen=3):
  global look
  for t in range(w):
    cl = []
    for c in range(t, size, w):
      cl.append(c)
    parseCons(cl, wLen)
  for l in range(0, size - w + 1, w):
    cl = []
    for r in range(l, l + w):
      cl.append(r)
    parseCons(cl, wLen)

  for t in range(w):
    cd2 = []
    cd = []
    d1 = t
    d2 = t
    while True:
      cd.append(d1)
      d1 += w + 1
      if d1 % w == 0 or d1 >= size: break
    while True:
      cd2.append(d2)
      d2 += w - 1
      if d2 % w == w - 1 or d2 >= size: break
    if len(cd) > 1: parseCons(cd, wLen)
    if len(cd2) > 1: parseCons(cd2, wLen)

  for l in range(w, size - w + 1, w):
    cl = []
    for d in range(l, size, w + 1):
      cl.append(d)
    if len(cl) > 1: parseCons(cl, wLen)

  for r in range(w * 2 - 1, size, w):
    cl = []
    for d in range(r, size - 1, w - 1):
      cl.append(d)
    if len(cl) > 1: parseCons(cl, wLen)


def winBoard(pzl, winNum, player):
  for s in look:
    cl = []
    for i in s:
      cl.append(pzl[i])
    if cl.count(player) == winNum: return True, player
  return False, 'x'


def print_board(board):
    for i in range(len(board)):
        if i % width == 0:
            print("")
        print(board[i], end="")
    print("")


def negamax(board):
    player = 'x' if board.count('x') == board.count('o') else 'o'
    terminal, winner = winBoard(board,3,other[player])
    if terminal:
        return {"W": set(), "L": board, "D": set()}
    if board.count('.') == 0:

        return {"W": set(), "L": set(), "D": board}
    result = {"W": set(), "L": set(), "D": set()}
    if board in cache:
        return cache[board]
    for i in range(len(board)):
        if board[i] == '.':
            newBoard = [*board]
            newBoard[i] = player
            cM = negamax(''.join(newBoard))
            brdCat = (cM["W"] and "L") or ( cM["D"] and "D") or "W"
            result[brdCat].add(i)
    cache[board] = result
    return  result

look = []
cache = {}
makeLookup(width,len(board),3)
res = negamax(board)
print(res)
