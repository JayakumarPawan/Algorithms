import sys
import re
import random
import math

from numpy import block

sys.setrecursionlimit(10000000)
WIDTH = 3
HEIGHT = 3
N_BLOCKS = 9
SEED_STRINGS = []
DICT_FILE = 'words.txt'
BLOCK = "#"
SPACE = "-"
PZL = 9 * SPACE

WORDS = {}
PREFIXES = {}
LETTER_FREQ = {i: 0 for i in 'abcdefghijklmnopqrstuvwxyz'}
WORD_LOC = [''] * 9
used = {}


def parse_cmd():
    """ set global variables found from the command line"""
    if len(sys.argv) > 3:
        global WIDTH
        WIDTH = int(re.search(r'(?<=x)\d*', sys.argv[1]).group(0))
        global HEIGHT
        HEIGHT = int(re.search(r'\d*(?=x)', sys.argv[1]).group(0))
        global N_BLOCKS
        N_BLOCKS = int(sys.argv[2])
        global DICT_FILE
        DICT_FILE = sys.argv[3]
        global SEED_STRINGS
        if len(sys.argv) > 3:
            SEED_STRINGS = sys.argv[4:]
        else:
            SEED_STRINGS = []
        global PZL
        PZL = HEIGHT * WIDTH * SPACE
        if HEIGHT * WIDTH == N_BLOCKS:
            print("#" * HEIGHT * WIDTH)
            exit()
        global WORD_LOC
        WORD_LOC = [''] * WIDTH * HEIGHT


def print_board(pzl):
    for i in range(len(pzl)):
        if i % WIDTH == 0:
            print("")
        print(pzl[i], end=" ")
    print("")


def rot_index_180(index):
    return len(PZL) - index % WIDTH - WIDTH * (index // WIDTH) - 1


def check_for_connectivity(pzl, index):
    if index % WIDTH in [0, WIDTH - 1] or index // WIDTH in [0, HEIGHT - 1]:
        return True
    if index % WIDTH - 1 >= 0 and pzl[index - 1] == BLOCK:
        return True
    if index % WIDTH + 1 < WIDTH and pzl[index + 1] == BLOCK:
        return True
    if index // WIDTH + 1 < HEIGHT and pzl[index + WIDTH] == BLOCK:
        return True
    if index // WIDTH - 1 >= 0 and pzl[index - WIDTH] == BLOCK:
        return True
    return False


def border_block(pzl, index):
    """ detects whether the block is so close to the border that words cant exist there"""
    go = [0, 0, 0, 0]  # go left right up down if 1
    if WIDTH == 3:
        return 0, 0
    if 0 < index % WIDTH < 3 and pzl[index - 1] != BLOCK or \
            index % WIDTH >= 3 and BLOCK in pzl[slice(index - 3, index - 1)] and pzl[index - 1] != BLOCK:
        go[0] = 1
    if WIDTH - 1 > index % WIDTH >= WIDTH - 3 and pzl[index + 1] != BLOCK or \
            index % WIDTH < WIDTH - 3 and BLOCK in pzl[slice(index + 2, index + 4)] and pzl[index + 1] != BLOCK:
        go[1] = 1
    if 0 < index // WIDTH < 3 and pzl[index - WIDTH] != BLOCK or \
            index // WIDTH >= 3 and BLOCK in pzl[slice(index - 3 * WIDTH, index - WIDTH, WIDTH)] and pzl[
        index - WIDTH] != BLOCK:
        go[2] = 1
    if HEIGHT - 1 > index // WIDTH >= HEIGHT - 3 and pzl[index + WIDTH] != BLOCK or \
            index // WIDTH < HEIGHT - 3 and BLOCK in pzl[slice(index + 2 * WIDTH, index + 3 * WIDTH + 1, WIDTH)] and \
            pzl[index + WIDTH] != BLOCK:
        go[3] = 1
    return go


def place_seed_strings():
    global PZL
    global WORD_LOC
    temp = [*PZL]
    blocks = []  # these blocks have to be here so make sure they fit the rules
    for seed in SEED_STRINGS:
        h = int(re.search(r'\d*(?=x)', seed).group(0))
        w = int(re.search(r'(?<=x)\d*', seed).group(0))
        orientation = seed[0]
        letters = seed[re.search(r'(?<=x)\d*', seed).end():].lower()
        if orientation.upper() == 'H':
            for i in range(len(letters)):
                temp[h * WIDTH + w + i] = letters[i]
                if i == 0:
                    WORD_LOC[h * WIDTH + w] = 's'
                if i == len(letters) - 1:
                    WORD_LOC[h * WIDTH + w + i] = 'e'
                if letters[i] == BLOCK:
                    blocks.append(h * WIDTH + w + i)
                    temp[rot_index_180(h * WIDTH + w + i)] = BLOCK
        if orientation.upper() == 'V':
            for i in range(len(letters)):
                temp[h * WIDTH + w + WIDTH * i] = letters[i]
                if i == 0:
                    WORD_LOC[h * WIDTH + w] = ''
                if i == len(letters) - 1:
                    WORD_LOC[h * WIDTH + w + WIDTH * i] = ''
                if letters[i] == BLOCK:
                    blocks.append(h * WIDTH + w + WIDTH * i)
                    temp[rot_index_180(h * WIDTH + w + WIDTH * i)] = BLOCK

    PZL = ''.join(temp)
    return blocks


def fill_small_gaps(pzl, anchors, n_blocks):
    temp = [*pzl]
    # This takes care of making sure there is enough space between blocks and borders
    for i in anchors:
        # print_board(temp)
        go = border_block(temp, i)
        if go[0]:
            temp[i - 1] = BLOCK
            temp[rot_index_180(i - 1)] = BLOCK
            n_blocks -= 2
            if i - 1 not in anchors:
                anchors.append(i - 1)
                anchors.append(rot_index_180(i - 1))
        if go[1]:
            temp[i + 1] = BLOCK
            temp[rot_index_180(i + 1)] = BLOCK
            n_blocks -= 2
            if i + 1 not in anchors:
                anchors.append(i + 1)
                anchors.append(rot_index_180(i + 1))
        if go[2]:
            temp[i - WIDTH] = BLOCK
            temp[rot_index_180(i - WIDTH)] = BLOCK
            n_blocks -= 2
            if i - WIDTH not in anchors:
                anchors.append(i - WIDTH)
                anchors.append(rot_index_180(i - WIDTH))
        if go[3]:
            temp[i + WIDTH] = BLOCK
            temp[rot_index_180(i + WIDTH)] = BLOCK
            n_blocks -= 2
            if i + WIDTH not in anchors:
                anchors.append(i + WIDTH)
                anchors.append(rot_index_180(i + WIDTH))
        if n_blocks < 0:
            return ''.join(temp), n_blocks

    return ''.join(temp), n_blocks


def is_connected(pzl):
    index = 0
    while(pzl[index] == BLOCK):
        index+=1
    visited = explore(pzl, index, set())
    # print(len(visited), HEIGHT * WIDTH - pzl.count(BLOCK))
    # print_board(pzl)
    return len(visited) >= HEIGHT * WIDTH - pzl.count(BLOCK)

def explore(pzl, index, visited):
    if index % WIDTH - 1 >= 0 and pzl[index - 1] != BLOCK and index - 1 not in visited:
        visited.add(index - 1)
        visited = explore(pzl, index - 1, visited)
    if index % WIDTH + 1 < WIDTH and pzl[index + 1] != BLOCK and index + 1 not in visited:
        visited.add(index + 1)
        visited = explore(pzl, index + 1, visited)
    if index // WIDTH + 1 < HEIGHT and pzl[index + WIDTH] != BLOCK and index + WIDTH not in visited:
        visited.add(index + WIDTH)
        visited = explore(pzl, index + WIDTH, visited)
    if index // WIDTH - 1 >= 0 and pzl[index - WIDTH] != BLOCK and index - WIDTH not in visited:
        visited.add(index - WIDTH)
        visited = explore(pzl, index - WIDTH, visited)
    return visited

def score_block_placement(pzl, i):
    # start filling the outside ring by spacing out and fitting as much as possible
    col,row = i%WIDTH, i // WIDTH
    score = 0
    if col == 0 or row == 0 or row == HEIGHT - 1 or col == WIDTH -1:
        score +=1000
    

    # put blocks next to only 1 other block
    block_count = 0
    if col != 0 and pzl[i-1] == BLOCK:
        block_count+= 1
    
    if col < WIDTH-1 and pzl[i+1] == BLOCK:
        block_count+= 1

    if row != 0 and pzl[i-WIDTH] == BLOCK:
        block_count+= 1

    if row < HEIGHT-1 and pzl[i+WIDTH] == BLOCK:
        block_count+= 1

    if block_count == 1:
        score += 5
    if block_count == 0:
        score +=10
    else:
        score -=5


    #space out blocks
    score -= 100* sum(border_block(pzl, i))

    j = i
    while pzl[j] != BLOCK and i-i%WIDTH < j < i-i%WIDTH+WIDTH:
        score+= 10
        j+=1
    j=i
    while pzl[j] != BLOCK and i-i%WIDTH < j < i-i%WIDTH+WIDTH:
        score+= 10
        j-=1



    return score

def fill_rest(pzl, n_blocks):
    print_board(pzl)
    if n_blocks == 0:
        return pzl
    best_spots = []
    for i in range(len(pzl) // 2 + len(pzl) % 2):
        if pzl[i] != SPACE or pzl[rot_index_180(i)] != SPACE:
            continue
        best_spots.append((i, score_block_placement(pzl, i)))

    best_spots.sort(key=lambda x: x[1], reverse=True)
    print(best_spots[:5])
    for i, _ in best_spots:
        sub_pzl = [*pzl]
        sub_pzl[i] = BLOCK
        sub_pzl[rot_index_180(i)] = BLOCK
        n_blocks -= 2
        sub_pzl, n = fill_small_gaps(sub_pzl, [i], n_blocks)
        if is_connected(pzl) and n > 0:
            # print_board(sub_pzl)
            bf = fill_rest(sub_pzl, n)
            if bf and is_connected(bf) and bf.count(BLOCK) == N_BLOCKS:
                return bf
    return ""


def make_pzl():
    parse_cmd()
    WORD_LOC = [''] * WIDTH * HEIGHT
    global PZL
    # print(f'width {WIDTH} height {HEIGHT} n {N_BLOCKS} dict {DICT_FILE}\n seed str {SEED_STRINGS}')
    anchor_blocks = place_seed_strings()
    PZL = [*PZL]
    # print(anchor_blocks)
    s = [rot_index_180(i) for i in anchor_blocks]
    # print(s)
    # print_board(PZL)
    PZL, blocks_left = fill_small_gaps(PZL, anchor_blocks, N_BLOCKS)
    # print_board(PZL)

    if PZL.find(SPACE) != -1:
        PZL = [*PZL]
        connected = explore(PZL, PZL.index(SPACE), {PZL.index(SPACE)})
        for j in range(len(PZL)):
            if j not in connected and PZL[j] == SPACE:
                PZL[j] = BLOCK
                blocks_left -= 1

    PZL = [*PZL]
    if N_BLOCKS % 2 == 1 == WIDTH % 2 == HEIGHT % 2:
        PZL[HEIGHT // 2 * WIDTH + WIDTH // 2] = BLOCK
        blocks_left -= 1
    PZL = ''.join(PZL)

    # print_board(PZL)
    # print("blocks left: ", N_BLOCKS - PZL.count(BLOCK))
    PZL = fill_rest(PZL, N_BLOCKS - PZL.count(BLOCK))
    PZL = PZL.replace('*', SPACE)
    # print_board(PZL)


make_pzl()
print_board(PZL)
print(PZL.count(BLOCK))