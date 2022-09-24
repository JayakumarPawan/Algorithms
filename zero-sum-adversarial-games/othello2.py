import sys

board = '.' * 27 + "ox......xo" + '.' * 27
player = 'x'
if len(sys.argv) > 2:
    board = sys.argv[1]
    player = sys.argv[2]
other = {'x': 'o', 'o': 'x'}

pos_weight = [40, -4, 4, 4, 4, 4, -4, 40,
              -4, -4, -1, -1, -1, -1, -4, -4,
              4, -1, 1, 0, 0, 1, -1, 4,
              4, -1, 0, 1, 1, 0, -1, 4,
              4, -1, 0, 1, 1, 0, -1, 4,
              4, -1, 1, 0, 0, 1, -1, 4,
              -4, -4, -1, -1, -1, -1, -4, -4,
              40, -4, 4, 4, 4, 4, -4, 40]


def update_weights():
    if board[0] == player:
        for i in range(5):
            pos_weight[1 + i] = 4
            pos_weight[8 + 8 * i] = 4
    if board[7] == player:
        for i in range(5):
            pos_weight[2 + i] = 4
            pos_weight[15 + 8 * i] = 4
    if board[63] == player:
        for i in range(5):
            pos_weight[58 + i] = 4
            pos_weight[23 + 8 * i] = 4
    if board[63] == player:
        for i in range(5):
            pos_weight[57 + i] = 4
            pos_weight[16 + 8 * i] = 4


def update(dict, key, val, merge):
    if key in dict:
        if merge:
            for i in val:
                dict[key].append(i)
        else:
            dict[key].append(val)
    else:
        if type(val) == list and merge:
            dict[key] = val
        else:
            dict[key] = [val]


def make_move(board, player, move, look_up):
    if move < 0:
        return board, player
    else:
        _, affected = valid_moves(board, player, look_up)
        if not affected:
            player = other[player]
            _, affected = valid_moves(board, player, look_up)
        board = [*board]
        for pos in affected[move]:
            board[pos] = player
        board = ''.join(board)
        return board, other[player]


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
            update(ref, i, row,False)
        for i in col:
            update(ref, i, col,False)

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
            update(ref, i, slash,False)
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
            update(ref, i, back,False)
    return look_up, ref


look_up, ref = look_up_generator()


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
                    update(affected, row[j + 1], row[i:j + 2], True)
                    moves.add(row[j + 1])
                j = i
                while j > 1 and board[row[j - 1]] == other[player]:
                    j -= 1
                if board[row[j]] == other[player] and board[row[j - 1]] in '*.':
                    board[row[j - 1]] = '*'
                    update(affected, row[j - 1], row[j - 1:i], True)
                    moves.add(row[j - 1])
    return board, affected


verbose = False


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


def negamax(board, player, level):
    _, moves = valid_moves(board, player, look_up)
    if not moves:
        _, moves = valid_moves(board, other[player], look_up)
        if not moves:
            return [board.count(player) - board.count(other[player])]
        else:
            return negamax(board, other[player],level+1)
    best = [-len(board)]
    for move in moves:
        nm = negamax(make_move(board,player,move,look_up)[0], other[player], level+1) + [move]
        if nm[0] > best[0]:
            best = nm
            #if not level:
                # print('score: {}'.format(nm))
    return best


def choose_move(board, player, look_up):
    update_weights()
    greedy = -.5
    if board.count('.') < 10:
        info = 2#negamax(board, player, 0)
        #print('choose_move score {}'.format(info))
    if board[0] == board[7] == board[63] == board[56] == player:
        greedy = 10
    _, moves_p1 = valid_moves(board, player, look_up)
    if not moves_p1:
        print("")
        return
    p1_move_scores = {}
    for move_p1, pieces_p1 in moves_p1.items():

        board_p1, enemy = make_move(board, player, move_p1, look_up)
        _, moves_e1 = valid_moves(board_p1, enemy, look_up)
        if verbose:
            print('move: ', move_p1)
            print('\tpos score: ', 10 * pos_weight[move_p1])
            print('\tenemy mobility score: ', (24 - len(moves_e1)))
            print('\tpiece capture  score: ', greedy * len(pieces_p1))
        p1_move_scores[move_p1] = 10 * pos_weight[move_p1]
        p1_move_scores[move_p1] += (24 - len(moves_e1))
        p1_move_scores[move_p1] += greedy * len(pieces_p1)
        stable_score = 0
        for piece in pieces_p1:
            if isStable(board_p1,player,piece):
                p1_move_scores[move_p1]+=5
                stable_score+=5
        if verbose:
            print('\tstable score: ',stable_score)
        if not moves_e1:
            _, moves_p2 = valid_moves(board_p1, player, look_up)
            p1_move_scores[move_p1] += len(moves_p2)
            continue
        e1_move_scores = {}

        for move_e1, pieces_e1 in moves_e1.items():
            e1_move_scores[move_e1] = 10 * pos_weight[move_e1] + len(pieces_e1)
        best_enemy_move = max(e1_move_scores, key=lambda key: e1_move_scores[key])
        board_e1, player = make_move(board_p1, enemy, best_enemy_move, look_up)
        for piece in pieces_e1:
            if isStable(board_e1, enemy, piece):
                e1_move_scores[move_e1] += 5
        if verbose:
            print('\tenemy best move score: ', -.5*best_enemy_move)
        p1_move_scores[move_p1] -= .5*e1_move_scores[best_enemy_move]

        _, moves_p2 = valid_moves(board_e1, player, look_up)

        p1_move_scores[move_p1] += len(moves_p2)
        if verbose:
            print('\tplayer mobility  score: ',len(moves_p2))
    if verbose:
        print('p1', p1_move_scores)

    print(max(p1_move_scores, key=lambda key: p1_move_scores[key]))


choose_move(board, player, look_up)





'''
def negamax(brd,tkn):
    a list where first item is score and the rest is a sequence of moves in reverse order (last move first)
    # return[minGuaranteedScore, seqLast, seqPenultimate, ...,seq2, seq1, seq0] 
    find possible moves
    if brd is terminal: return [score]
    if not possibleMoves: deal with a forced pass
    #nmLIst is a list of negamax results
    nmLIst = [negamax(makeMove(brd,tkn,mv), enemyTkn) + [mv] for mv in possibleMoves]
    best = sorted(nmList)[appropriateIndex]
    return appropriate sequence based on best
'''
