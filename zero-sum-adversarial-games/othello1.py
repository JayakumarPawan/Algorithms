import sys

other = {'x': 'o', 'o': 'x'}
board = '.' * 27 + "ox......xo" + '.' * 27
player = 'x'
moves = []
pos_weight = [4, -2, 3, 3, 3, 3, -2, 4,
              -2, -4, -1, -1, -1, -1, -2, -4,
              3, -1, 1, 0, 0, 1, -1, 3,
              3, -1, 0, 1, 1, 0, -1, 3,
              3, -1, 0, 1, 1, 0, -1, 3,
              3, -1, 1, 0, 0, 1, -1, 3,
              -2, -4, -1, -1, -1, -1, -2, -4,
              4, -2, 3, 3, 3, 3, -2, 4]

pos_coeff = 4
mob_coeff = 3
center_coeff = 1
stability_coeff = 2
capture_coeff  = -2
frontier_coeff = 2
corner_coeff = 3


def a1_to_index(a1):
    if a1[0] in {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}:
        return 8 * (int(a1[1]) - 1) + ord(a1[0]) - 97
    else:
        return int(a1)


if len(sys.argv) == 2:
    if len(sys.argv[1]) == 64:
        board = sys.argv[1].lower()
        player = 'o' if board.count('.') % 2 == 1 else 'x'
    elif sys.argv[1].lower() in other:
        player = sys.argv[1].lower()
    else:
        moves = sys.argv[1].lower()
if len(sys.argv) == 3:
    if len(sys.argv[1]) > 3:
        board = sys.argv[1].lower()
        if sys.argv[2].lower() in other:
            player = sys.argv[2].lower()
        else:
            moves = [a1_to_index(sys.argv[2].lower())]
            player = 'o' if board.count('.') % 2 == 1 else 'x'
    elif sys.argv[1].lower() in other:
        player = sys.argv[1].lower()
        moves = [a1_to_index(sys.argv[2].lower())]
    else:
        moves = [a1_to_index(i.lower()) for i in sys.argv[1:]]
if len(sys.argv) >= 4:
    if len(sys.argv[1]) > 3:
        board = sys.argv[1].lower()
        if sys.argv[2].lower() in other:
            player = sys.argv[2].lower()
            moves = [a1_to_index(i.lower()) for i in sys.argv[3:]]
        else:
            player = 'o' if board.count('.') % 2 == 1 else 'x'
            moves = [a1_to_index(i.lower()) for i in sys.argv[2:]]
    elif sys.argv[1].lower() in other:
        player = sys.argv[1].lower()
        moves = [a1_to_index(i.lower()) for i in sys.argv[2:]]
    else:
        moves = [a1_to_index(i.lower()) for i in sys.argv[1:]]


'''
0  1  2  3  4  5  6  7
8  9  10 11 12 13 14 15
16 17 18 19 20 21 22 23
24 25 26 27 28 29 30 31
32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47
48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63
'''  # index grid


def update(dict, key, val):
    if key in dict:
        dict[key].append(val)
    else:
        dict[key] = [val]


def look_up_generator():
    look_up = []
    ref = {}
    for i in range(8):
        row = []
        col = []
        slash = []
        back = []
        for j in range(8):
            row.append(i * 8 + j)
            col.append(j * 8 + i)
        look_up.append(row)
        look_up.append(col)
        for i in row:
            update(ref, i, row)
        for i in col:
            update(ref, i, col)

    for i in {2, 3, 4, 5, 6, 7, 15, 23, 31, 39, 47}:
        slash = []
        ix = i % 8
        iy = i // 8
        while 0 <= ix < 8 and 0 <= iy < 8:
            slash.append(ix + iy * 8)
            ix -= 1
            iy += 1
        look_up.append(slash)
        for i in slash:
            update(ref, i, slash)
    for i in {40, 32, 24, 16, 8, 0, 1, 2, 3, 4, 5}:
        back = []
        ix = i % 8
        iy = i // 8
        while 0 <= ix < 8 and 0 <= iy < 8:
            back.append(ix + iy * 8)
            ix += 1
            iy += 1
        look_up.append(back)
        for i in back:
            update(ref, i, back)
    return look_up, ref


def valid_moves(board, player, look_up):
    moves = set()
    affected = {}
    board = [*board]
    for row in look_up:
        for i in range(len(row)):
            if board[row[i]] == player:
                j = i
                while j + 1 < len(row) and board[row[j + 1]] == other[player]:
                    j += 1
                if j + 1 < len(row) and board[row[j]] == other[player] and board[row[j + 1]] in '*.':
                    board[row[j + 1]] = '*'
                    update(affected, row[j + 1], row[i:j + 2])
                    moves.add(row[j + 1])
                j = i
                while j > 1 and board[row[j - 1]] == other[player]:
                    j -= 1
                if board[row[j]] == other[player] and board[row[j - 1]] in '*.':
                    board[row[j - 1]] = '*'
                    update(affected, row[j - 1], row[j-1:i])
                    moves.add(row[j - 1])
    return board, affected


def print_board(board):
    for i in range(len(board)):
        if i % 8 == 0:
            print("")
        print(board[i], end=" ")
    print("")


def make_move(board, player, move, look_up):
    if move < 0:
        return board, player
    else:
        _, affected = valid_moves(board, player, look_up)
        if not affected:
            player = other[player]
            _, affected = valid_moves(board, player, look_up)
        board = [*board]
        for dir in affected[move]:
            for pos in dir:
                board[pos] = player
        board = ''.join(board)
        return board, other[player]


def isStable(board, player, piece):
    if piece in [0, 7, 63, 56] and board[piece] == player:
        return True
    if piece in [0, 1, 2, 3, 4, 5, 6, 7, 56, 57, 58, 59, 60, 61, 62, 63]:
        if board[piece - piece % 8: piece + 1] == player * (1 + piece % 8):
            return True
        if board[piece: piece + 7 - piece % 8] == player * (1 + piece % 8):
            return True
    if piece in [0, 8, 16, 24, 32, 40, 48, 56]:
        if board[slice(piece, 57, 8)] == player * (8 - piece // 8):
            return True
        if board[slice(0, piece + 1, 8)] == player * (piece // 8 + 1):
            return True
    if piece in [7, 15, 23, 31, 39, 47, 55, 63]:
        if board[slice(piece, 64, 8)] == player * (8 - piece // 8):
            return True
        if board[slice(7, piece + 1, 8)] == player * (piece // 8 + 1):
            return True
    return False


def is_frontier(board, pos):
    if pos % 8 - 1 >=0:
        if board[pos-1] == '.':
            return True
        if pos // 8 - 1 >= 0 and board[pos-9] =='.':
            return True
        if pos // 8 + 1 < 8 and board[pos+7] =='.':
            return True

    if pos % 8 +1 < 8:
        if board[pos+1] == '.':
            return True
        if pos // 8 - 1 >= 0 and board[pos-7] =='.':
            return True
        if pos // 8 + 1 < 8 and board[pos+9] =='.':
            return True

    if pos // 8 - 1 >= 0 and board[pos-8] == '.':
        return True
    if pos // 8 + 1 < 8 and board[pos+8] == '.':
        return True
    return False


def eval_board(board, player, look_up):
    pos_score = 0
    center_score = 0
    stability_score = 0
    capture_score = 0
    frontier_score = 0
    corner_score = 0
    for i in range(len(board)):
        if board[i] == player:
            pos_score += pos_weight[i]
            if isStable(board, player, i):
                stability_score += 1
            capture_score += 1
            if is_frontier(board, i):
                frontier_score += 1
    moves = valid_moves(board, player, look_up)
    opp_moves = valid_moves(board, other[player], look_up)
    mobility_score = len(moves) - len(opp_moves)

    for i in [18, 19, 20, 21, 25, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45]:
        if board[i] == player:
            center_score += 1

    for i in [0,7,63,56]:
        if i in moves or board[i] == player:
            corner_score +=1
        if board[i] == other[player]:
            corner_score -=2
    print('stability score: ', stability_score * stability_coeff, "mobility score: ", mobility_score * mob_coeff,"Frontier score: ", frontier_score * frontier_coeff)
    return pos_score * pos_coeff \
           + mobility_score * mob_coeff \
           + center_score * center_coeff \
           + stability_score * stability_coeff \
           + capture_score * capture_coeff \
           + frontier_score * frontier_coeff \
           + corner_score * corner_coeff


def snapshot(board, player, move, look_up):
    if move >= 0:
        print("{} plays to {}".format(other[player], move))
    possibles, affected = valid_moves(board, player, look_up)
    if not affected:
        player = other[player]
        possibles, affected = valid_moves(board, player, look_up)
    print_board(possibles)
    print(board)
    print("{}/{}".format(board.count('x'), board.count('o')))
    if affected:
        print("Possible moves for {}: {}".format(player, ', '.join([str(i) for i in affected.keys()])))
    print("evaluation: ", eval_board(board, player, look_up))


def othelloA(board,player):
    look_up, ref = look_up_generator()
    snapshot(board, player, -1,look_up)

    for move in moves:
        if move < 0:
            continue
        board, player = make_move(board,player,move,look_up)
        snapshot(board, player, move,look_up)


#othelloA(board, player)

def replay_viewer(game_str, board, player):
    look_up, ref = look_up_generator()
    snapshot(board, player, -1, look_up)
    moves = [game_str[i:i+2] for i in range(0, len(game_str), 2)]
    for move in moves:
        if '_' in move:
            move = int(move[-1])
        move = int(move)
        if move < 0:
            continue
        board, player = make_move(board, player, move, look_up)
        snapshot(board, player, move, look_up)

replay_viewer(moves, board, player)