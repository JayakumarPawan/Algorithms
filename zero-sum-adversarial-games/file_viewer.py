import sys
other = {'@':'o', 'o':'@', 'null': 'null','.':'.'}
change = {'@': 'x', 'o':'o','.':'.'}
dict = {}

def joe(index):
    return 8 * (index // 10 - 1) + (index % 10 -1 )


def convert_to_8x8(board):
    board = "".join([board[i:i + 8] for i in range(11, 91, 10)])
    board = [*board]
    for i in range(len(board)):
        board[i] = change[board[i]]
    board = ''.join(board)
    return board


f = open('games.txt', "r").read().splitlines()


for l in range(len(f)):
    move = f[l].split(' ')
    dict[(convert_to_8x8(move[0]), change[move[1]])] = joe(int(move[-1]))


def convert_to_10x10(index):
    return 10 * (index // 8 + 1) + (index % 8 + 1)
def joe(index):
    return 8 * (index // 10 - 1) + (index % 10 -1 )


board = '.' * 27 + "ox......xo" + '.' * 27
player = 'x'
if len(sys.argv) > 2:
    board = sys.argv[1]
    player = sys.argv[2]

for k,v in dict.items():
    print(f'{k} : {v},')