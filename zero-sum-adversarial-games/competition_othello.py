import sys
openning_book = {
('...........................ox......xo...........................', 'x') : 19,
('..................ox.......ox......xo...........................', 'x') : 26,
('..................ooo.....xxo......xo...........................', 'x') : 11,
('..........ox......ooo.....xxo......xo...........................', 'x') : 12,
('..........oooo....oxo.....xxo......xo...........................', 'x') : 17,
('..........oooo...xoxo....oooo......xo...........................', 'x') : 3,
('...x......xxoo...xoxo....oooo.....ooo...........................', 'x') : 32,
('..ox......oooo...xoxo....xooo...x.ooo...........................', 'x') : 1,
('.xxx......xooo..oooxo....oooo...x.ooo...........................', 'x') : 4,
('.xxxx.....xxoo..ooxxo....oooo...xoooo...........................', 'x') : 5,
('.xxxxx...ooooo..oooxo....oooo...xoooo...........................', 'x') : 22,
('.xxxxx...oooooo.oooxo.x..oooo...xoooo...........................', 'x') : 23,
('.xxxxx...ooooox.oooxo.ox.oooo..oxoooo...........................', 'x') : 39,
('.xxxxxo..oooooo.oooxo.ox.oooo..xxoooo..x........................', 'x') : 7,
('.xxxxxxx.oooooo.oooxo.ox.oooo..xxoooo..x........................', 'x') : 42,
('.xxxxxxx.oxoooo.ooxxo.ox.oxoo..xxoooo..x.ox.....................', 'x') : 15,
('.xxxxxxx.oxxxxxxooxxo.ox.oxoo..xxoooo..x.ooo....................', 'x') : 0,
('xxxxxxxx.xxxxxxxooxxo.ox.oxoo..xxoooo..x.ooo....................', 'x') : 8,
('xxxxxxxxxxxxxxxxoxxxo.ox.oxoo..xxoooo..x.ooo....................', 'x') : 24,
('xxxxxxxxxxxxxxxxxxxxo.oxxxxoo..xxoooo..x.ooo....................', 'x') : 40,
('xxxxxxxxxxxxxxxxxxxxo.oxxxxoo..xxxooo..xxooo....................', 'x') : 21,
('xxxxxxxxxxxxxxxxxxxxxxxxxxxoo..xxxooo..xxooo....................', 'x') : 29,
('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxooo..xxooo....................', 'x') : 37,
('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxx.xxooo....................', 'x') : 44,
('...................x.......xx......xo...........................', 'o') : 34,
('...................x.......xx.....xoo....x......................', 'o') : 21,
('...................x.o.....xxx....xoo....x......................', 'o') : 20,
('...........x.......xxo.....xox....xoo....x......................', 'o') : 37,
('...........x.......xxxx....xoo....xooo...x......................', 'o') : 12,
('...........xxx.....xxxx....xoo....xooo...x......................', 'o') : 26,
('...........xxx....xxxxx...xooo....xooo...x......................', 'o') : 10,
('..........oxxx....xoxxx...xxxxx...xooo...x......................', 'o') : 4,
('....o.....oxox....xooxx...xxoxx...xxxxx..x......................', 'o') : 3,
('..xoo.....xxox....xoxxx...xxoxx...xxxxx..x......................', 'o') : 1,
('.oooox....oxxx....xxxxx...xxoxx...xxxxx..x......................', 'o') : 6,
('.oooooo..xxxxx....xxxxx...xxoxx...xxxxx..x......................', 'o') : 25,
('.oooooo..xxoxx...xxxxxx..oxooxx...xxxxx..x......................', 'o') : 0,
('ooooooo..oxoxx...xoxxxx..xxooxx..xxxxxx..x......................', 'o') : 40,
('ooooooo..oxoox...xooxxx..xoooxx.xxxxxxx.ox......................', 'o') : 8,
('ooooooo.ooxoox..xxxxxxx..xoooxx.xxxxxxx.ox......................', 'o') : 24,
('ooooooo.ooooox..ooxxxxx.oooooxx.oxxxxxx.ox......................', 'o') : 49,
('ooooooo.ooooox..ooxxxxx.oooooxx.ooxxxxx.ox......xo..............', 'o') : 56,
('ooooooo.ooooox..ooxxxxx.oooooxx.ooxxxxx.ox......ox......ox......', 'o') : 58,
('ooooooo.ooooox..ooxxxxx.oooooxx.ooxxxxx.oo......ooo.....ooo.....', 'o') : 42,
('ooooooo.ooooox..ooxxxxx.oooxoxx.oooxxxx.ooox....ooo.....ooo.....', 'o') : 51,
('ooooooo.ooooox..ooxoxxx.oooooxx.ooooxxx.oooo....oooo....ooo.....', 'o') : 14,
('ooooooo.ooooooo.ooxoxox.oooooxx.ooooxxx.oooo....oooo....ooo.....', 'o') : 23,
('ooooooo.oooooooxooxoxoxooooooxx.ooooxxx.oooo....oooo....ooo.....', 'o') : 7,
('ooooooooooooooooooxoxoxooooooxx.ooooxxx.oooo....oooo....ooo.....', 'o') : 47,
('ooooooooooooooooooxoooxooooooox.ooooxxx.oooo..xooooo....ooo.....', 'o') : 31,
('ooooooooooooooooooxoooooooooooooooooxxx.oooo..xooooo....ooo.....', 'o') : 39,
('ooooooooooooooooooxooooooooxooooooooxooooooo.xxooooo....ooo.....', 'o') : 54,
('ooooooo.ooooox..ooxxxxx.oooooxx.ooxxxxx.ox......oo......ooo.....', 'o') : 50,
('ooooooo.ooooox..ooxxxxx.oooooxx.ooxxxxx.oo......ooo.....ooo.....', 'o') : 42,
('ooooooo.ooooox..ooxxxxx.oooxoxx.oooxxxx.ooox....ooo.....ooo.....', 'o') : 51,
('ooooooo.ooooox..ooxoxxx.oooooxx.ooooxxx.oooo....oooo....ooo.....', 'o') : 14,
('ooooooo.ooooooo.ooxoxox.oooooxx.ooooxxx.oooo....oooo....ooo.....','o') : 23,
('ooooooo.oooooooxooxoxoxooooooxx.ooooxxx.oooo....oooo....ooo.....', 'o') : 7,
('ooooooooooooooooooxoxoxooooooxx.ooooxxx.oooo....oooo....ooo.....', 'o') : 47,
('ooooooooooooooooooxoooxooooooox.ooooxxx.oooo..xooooo....ooo.....', 'o') : 31,
('ooooooooooooooooooxoooooooooooooooooxxx.oooo..xooooo....ooo.....', 'o') : 39,
('ooooooooooooooooooxooooooooxooooooooxooooooo.xxooooo....ooo.....', 'o') : 54
}


other = {'@': 'o', 'o': '@'}
pos_weight = [400, -10, 3, 3, 3, 3, -10, 400,
              -10, -15, -1, -1, -1, -1, -15, -10,
              3, -1, 1, 0, 0, 1, -1, 3,
              3, -1, 0, 1, 1, 0, -1, 3,
              3, -1, 0, 1, 1, 0, -1, 3,
              3, -1, 1, 0, 0, 1, -1, 3,
              -10, -15, -1, -1, -1, -1, -15, -10,
              400, -10, 3, 3, 3, 3, -10, 400]
move_cache = {}
ab_cache = {}

pos_coeff = 10
mob_coeff = 8
center_coeff = 5
stability_coeff = 5
capture_coeff  = -3
frontier_coeff = -7
corner_coeff = 10


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
    return affected


def convert_to_12x12(index):
    return 10 * (index // 8 + 1) + (index % 8 + 1)


def convert_to_8x8(board):
    return "".join([board[i:i + 8] for i in range(11, 91, 10)])


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


def print_board(board):
    for i in range(len(board)):
        if i % 8 == 0:
            print("")
        print(board[i], end=" ")
    print("")


def look_up_generator():
    look_up = []
    ref = {}
    for i in range(8):
        row = []
        col = []
        for j in range(8):
            row.append(i * 8 + j)
            col.append(j * 8 + i)
        look_up.append(row)
        look_up.append(col)
        for i in row:
            update(ref, i, row, False)
        for i in col:
            update(ref, i, col, False)

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
            update(ref, i, slash, False)
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
            update(ref, i, back, False)
    return look_up, ref


look_up, ref = look_up_generator()


def make_move(board, player, move, look_up):
    if move < 0:
        return board, player
    else:
        affected = valid_moves(board, player, look_up)
        if not affected:
            player = other[player]
            affected = valid_moves(board, player, look_up)
        board = [*board]
        for pos in affected[move]:
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


def eval_board(board, player):
    pos_score = 0
    opp_pos_score = 0
    center_score = 0
    opp_center_score = 0
    stability_score = 0
    opp_stability_score =0
    capture_score = 0
    opp_capture_score = 0
    frontier_score = 0
    opp_frontier_score = 0
    corner_score = 0
    opp_corner_score = 0

    for i in range(len(board)):
        if board[i] == player:
            pos_score += pos_weight[i]
            if isStable(board, player, i):
                stability_score += 1
            capture_score += 1
            if is_frontier(board, i):
                frontier_score += 1
        if board[i] == other[player]:
            opp_pos_score += pos_weight[i]
            if isStable(board, other[player], i):
                opp_stability_score += 1
            opp_capture_score += 1
            if is_frontier(board, i):
                opp_frontier_score += 1
    moves = valid_moves(board, player, look_up)
    opp_moves = valid_moves(board, other[player], look_up)


    for i in [18, 19, 20, 21, 25, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45]:
        if board[i] == player:
            center_score += 1
        if board[i] == other[player]:
            opp_center_score +=1

    for i in [0,7,63,56]:
        if i in moves or board[i] == player:
            corner_score += 1
        if i in opp_moves or board[i] == other[player]:
            corner_score += 1
    pos = pos_coeff * (pos_score - opp_pos_score) / (pos_score + opp_pos_score) if pos_score + opp_pos_score != 0 else 0
    mobile = mob_coeff * (len(moves) - len(opp_moves)) / (len(moves) + len(opp_moves)) if len(moves) + len(opp_moves) != 0 else 0
    center = center_coeff * (center_score - opp_center_score) / (center_score + opp_center_score) if center_score + opp_center_score != 0 else 0
    stable = stability_coeff * (stability_score - opp_stability_score) / (stability_score + opp_stability_score) if stability_score+opp_stability_score != 0 else 0
    capture = capture_coeff * (capture_score - opp_capture_score) / (capture_score + opp_capture_score)
    frontier = frontier_coeff * (frontier_score - opp_frontier_score) / (frontier_score + opp_frontier_score) if frontier_score + opp_frontier_score != 0 else 0
    corner = corner_coeff * (corner_score - 5 * opp_corner_score)
    return pos + mobile + center + stable + capture + frontier + corner


def mid_alpha_beta(board, player, depth, alpha, beta, best_move):
    if depth == 0:
        return [eval_board(board, player)]
    if (board, player) in move_cache:
        moves = move_cache[(board, player)]
    else:
        moves = valid_moves(board, player, look_up)
        move_cache[(board, player)] = moves
    if not moves:
        moves = valid_moves(board, other[player], look_up)
        move_cache[(board, other[player])] = moves
        if not moves:
            return [10000] if board.count(player) > board.count(other[player]) else [-10000]  # win or lose very good/bad
        else:
            ab = mid_alpha_beta(board, other[player], depth - 1, -beta, -alpha, best_move) + [-1]
            score = -ab[0]
            if score < alpha:
                return [score]
            if score > beta:
                return [score]
            return [score] + ab[1:]

    if (board, player, alpha, beta) in ab_cache:
        return ab_cache[(board, player, alpha, beta)]

    best = [alpha - 1]
    for move in moves:
        new_board, enemy = make_move(board, player, move, look_up)
        ab = mid_alpha_beta(new_board, other[player], depth - 1, -beta, -alpha, best_move)
        score = -ab[0]
        if score > beta:
            return [score]
        if score < alpha:
            continue
        alpha = score + 1
        best = [score] + ab[1:] + [move]
        if depth == 4:
            best_move.value = best[-1]
    ab_cache[(board, player, alpha, beta)] = best
    return best


def terminal_alpha_beta(board, player, level, alpha, beta, best_move):
    if (board, player) in move_cache:
        moves = move_cache[(board, player)]
    else:
        moves = valid_moves(board, player, look_up)
        move_cache[(board, player)] = moves
    if not moves:
        moves = valid_moves(board, other[player], look_up)
        move_cache[(board, other[player])] = moves
        if not moves:
            return [board.count(player) - board.count(other[player])]
        else:
            ab = terminal_alpha_beta(board, other[player], level + 1, -beta, -alpha, best_move) + [-1]
            score = -ab[0]
            if score < alpha:
                return [score]
            if score > beta:
                return [score]
            return [score] + ab[1:]

    if (board, player, alpha, beta) in ab_cache:
        return ab_cache[(board, player, alpha, beta)]

    best = [alpha - 1]
    for move in moves:
        new_board, enemy = make_move(board, player, move, look_up)
        ab = terminal_alpha_beta(new_board, other[player], level + 1, -beta, -alpha, best_move)
        score = -ab[0]
        if score > beta:
            return [score]
        if score < alpha:
            continue
        if not level and best[-1] in moves:
            best_move.value = best[-1]
        alpha = score + 1
        best = [score] + ab[1:] + [move]
    ab_cache[(board, player, alpha, beta)] = best
    best_move.value = best[-1]
    return best


def mid_alpha_beta1(board, player, depth, alpha, beta):
    if depth == 0:
        score = eval_board(board, player)
        return [score]
    if (board, player) in move_cache:
        moves = move_cache[(board, player)]
    else:
        moves = valid_moves(board, player, look_up)
        move_cache[(board, player)] = moves
    if not moves:
        moves = valid_moves(board, other[player], look_up)
        move_cache[(board, other[player])] = moves
        if not moves:
            return 10000 if board.count(player) > board.count(
                other[player]) else -10000  # win or lose very good/bad
        else:
            ab = mid_alpha_beta1(board, other[player], depth - 1, -beta, -alpha) + [-1]
            score = -ab[0]
            if score < alpha:
                return [score]
            if score > beta:
                return [score]
            return [score] + ab[1:]

    if (board, player, alpha, beta) in ab_cache:
        return ab_cache[(board, player, alpha, beta)]

    best = [alpha - 1]
    for move in moves:
        new_board, enemy = make_move(board, player, move, look_up)
        ab = mid_alpha_beta1(new_board, other[player], depth - 1, -beta, -alpha)
        score = -ab[0]
        if score > beta:
            return [score]
        if score < alpha:
            continue
        alpha = score + 1
        best = [score] + ab[1:] + [move]
        if depth == 4 and best[-1] in moves:
            print(best[-1])
    ab_cache[(board, player, alpha, beta)] = best
    return best


def terminal_alpha_beta1(board, player, level, alpha, beta):
    if (board, player) in move_cache:
        moves = move_cache[(board, player)]
    else:
        moves = valid_moves(board, player, look_up)
        move_cache[(board, player)] = moves
    if not moves:
        moves = valid_moves(board, other[player], look_up)
        move_cache[(board, other[player])] = moves
        if not moves:
            return [board.count(player) - board.count(other[player])]
        else:
            ab = terminal_alpha_beta1(board, other[player], level + 1, -beta, -alpha) + [-1]
            score = -ab[0]
            if score < alpha:
                return [score]
            if score > beta:
                return [score]
            return [score] + ab[1:]

    if (board, player, alpha, beta) in ab_cache:
        return ab_cache[(board, player, alpha, beta)]

    best = [alpha - 1]
    for move in moves:
        new_board, enemy = make_move(board, player, move, look_up)
        ab = terminal_alpha_beta1(new_board, other[player], level + 1, -beta, -alpha)
        score = -ab[0]
        if score > beta:
            return [score]
        if score < alpha:
            continue
        if not level:
            print(best[-1])
        alpha = score + 1
        best = [score] + ab[1:] + [move]
    ab_cache[(board, player, alpha, beta)] = best
    return best


class Strategy:

    def best_strategy(self, board, player, best_move, running):
        board = convert_to_8x8(board)
        #best_move.value = convert_to_12x12(max(valid_moves(board, player, look_up)))
        if (board,player) in openning_book:
            best_move.value = openning_book[(board,player)]
        elif board.count('.') < 10:
            best_move.value = terminal_alpha_beta(board, player, 0, -64, 64, best_move)[-1]
        else:
            best_move.value = mid_alpha_beta(board, player, 4, -10000, 10000, best_move)[-1]
        best_move.value = convert_to_12x12(best_move.value)


if __name__ == '__main__':
    board = '.' * 27 + "ox......xo" + '.' * 27
    player = 'x'
    if len(sys.argv) > 2:
        board = sys.argv[1]
        player = sys.argv[2]
    other = {'x': 'o', 'o': 'x'}

    move_cache = {}
    ab_cache = {}
    if (board,player) in openning_book:
        print(openning_book[(board,player)])
    elif board.count('.') < e:
        ab = terminal_alpha_beta1(board, player, 0, -64, 64)[-1]
        print(ab)
    else:
        ab = mid_alpha_beta1(board, player, 2, -10000, 10000)[-1]
        print(ab)
