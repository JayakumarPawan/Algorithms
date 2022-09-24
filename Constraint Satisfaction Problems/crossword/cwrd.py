import sys
import re
import random

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


def is_connected(pzl, index, visited):
    if index % WIDTH - 1 >= 0 and pzl[index - 1] != BLOCK and index - 1 not in visited:
        visited.append(index - 1)
        visited = is_connected(pzl, index - 1, visited)
    if index % WIDTH + 1 < WIDTH and pzl[index + 1] != BLOCK and index + 1 not in visited:
        visited.append(index + 1)
        visited = is_connected(pzl, index + 1, visited)
    if index // WIDTH + 1 < HEIGHT and pzl[index + WIDTH] != BLOCK and index + WIDTH not in visited:
        visited.append(index + WIDTH)
        visited = is_connected(pzl, index + WIDTH, visited)
    if index // WIDTH - 1 >= 0 and pzl[index - WIDTH] != BLOCK and index - WIDTH not in visited:
        visited.append(index - WIDTH)
        visited = is_connected(pzl, index - WIDTH, visited)
    return visited


def fill_rest(pzl, n_blocks):
    #print(pzl)
    if n_blocks == 0:
        return pzl
    best_spots = []
    for i in range(len(pzl) // 2 + len(pzl) % 2):
        if pzl[i] != SPACE or pzl[rot_index_180(i)] != SPACE:
            continue
        # j = i
        # space_count = 0
        # while j % WIDTH != WIDTH - 1 and pzl[j] != BLOCK:
        #     space_count += 1
        #     j += 1
        # j = i
        # while j % WIDTH != 0 and pzl[j] != BLOCK:
        #     space_count += 1
        #     j -= 1
        # j = i
        # while j < len(pzl) and pzl[j] != BLOCK:
        #     space_count += 1
        #     j += WIDTH
        # j = i
        # while j >= 0 and pzl[j] != BLOCK:
        #     space_count += 1
        #     j -= WIDTH
        space_count = 0
        if i % WIDTH == 0:
            space_count -= 5
        if i % WIDTH == WIDTH - 1:
            space_count -= 5
        if i // WIDTH == 0:
            space_count -= 5
        if i // WIDTH == HEIGHT - 1:
            space_count -= 5
        sub_pzl = [*pzl]
        sub_pzl[i] = BLOCK
        sub_pzl[rot_index_180(i)] = BLOCK
        n_blocks = N_BLOCKS - sub_pzl.count(BLOCK)
        sub_pzl, n = fill_small_gaps(sub_pzl, [i], n_blocks)

        best_spots.append((i, random.randint(0, len(pzl) - (n_blocks - n) + space_count)))
    best_spots.sort(key=lambda x: x[1], reverse=True)

    for i, space_count in best_spots:
        sub_pzl = [*pzl]
        sub_pzl[i] = BLOCK
        sub_pzl[rot_index_180(i)] = BLOCK
        # print_board(sub_pzl)
        n_blocks = N_BLOCKS - sub_pzl.count(BLOCK)
        sub_pzl, n = fill_small_gaps(sub_pzl, [i], n_blocks)
        if n >= 0 and len(is_connected(sub_pzl, i, [])) >= HEIGHT * WIDTH - N_BLOCKS:
            bf = fill_rest(sub_pzl, n)
            if bf:
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
        connected = is_connected(PZL, PZL.index(SPACE), [PZL.index(SPACE)])
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


def make_prefixes(word):
    """
    make a dictionary bin words by length then by the words that have the words with a,b,c,d...etc in the first spot
    a,b,c,d...etc in the second spot, and so on for all lengths of words

    dict[lenght of word][position][letter] = [words with this constraint sorted by 'goodness']

    """
    global PREFIXES
    if len(word) not in PREFIXES:
        PREFIXES[len(word)] = {}
    for pos, letter in enumerate(word):
        if (pos, letter) not in PREFIXES[len(word)]:
            PREFIXES[len(word)][(pos, letter)] = set()
        PREFIXES[len(word)][(pos, letter)].add(word)


def parse_words():
    global WORDS
    global PREFIXES
    WORDS = {}  # = { 'a' : {5: ['apple'], 3:['and','app']}} words in the list are sorted by commonality of letters
    global LETTER_FREQ
    words_file = open(r'words.txt', "r").read().splitlines()
    # words_file = open(DICT_FILE, "r").read().splitlines()
    for word in words_file:
        if len(word) >= 3:
            if len(word) not in WORDS:
                WORDS[len(word)] = {word}
            else:
                WORDS[len(word)].add(word)
            for letter in word.lower():
                LETTER_FREQ[letter] += 1
        make_prefixes(word)


def find_options_for_all_locations(pzl, used):
    final_options = []  # pos: list of tuples where first element is orientation 2nd is word 3rd is position
    position = pzl.find(SPACE)
    while position % WIDTH and pzl[position - 1] in 'abcdefghijklmnopqrstuvwxyz' and WORD_LOC[position - 1] != 'e':
        position -= 1

    pos_options = []
    w_h = True  # possible for horizontal

    # find the closest obstacle in right or down (border or block):

    block_pos = pzl.find(BLOCK, position)
    if block_pos != -1:
        max_len_h = min(block_pos, position - position % WIDTH + WIDTH) - position
    else:  # no block so just border
        max_len_h = WIDTH - position % WIDTH

    if max_len_h < 3:
        w_v = False
    # options = all words that start with token and are small enough:
    if w_h:
        options_h = set()
        for i in range(3, max_len_h + 1):
            if i not in [max_len_h - 2, max_len_h - 1]:
                options_h |= WORDS[i]
        options_h -= used
        # ensure word matches existing stuff if so add to final options
        for word in options_h:
            use = True
            for i, letter in enumerate(word):
                # check if the word is attempting to override existing letters
                if not (pzl[position + i] == letter or pzl[position + i] == SPACE):
                    use = False
                    break
            if use:
                pos_options.append(('H', word, position))
    # sort words based on freq of letters (sum([frequency(letter) for letter in word]))
    pos_options.sort(
        key=lambda x: sum([LETTER_FREQ[i] // 1000 for i in x[1].lower()]) + 300 * (len(set(x[1])) - len(x[1])),
        reverse=True)
    # print(pos_options)
    final_options.append(pos_options)
    # sort final_options tuples by the number of options in that position
    final_options.sort(key=lambda x: len(x))
    return final_options


def fill_words(pzl, used):
    print_board(pzl)
    if pzl.find(SPACE) == -1:
        return pzl

    word_options = find_options_for_all_locations(pzl, used)
    for option in word_options:
        for word in option:
            sub_pzl = [*pzl]
            WORD_LOC[word[2]] = 's'
            WORD_LOC[word[2] + len(word[1]) - 1] = 'e'
            for i, letter in enumerate(word[1]):
                sub_pzl[word[2] + i] = letter
            used.add(word[1])
            print(word[1])
            bf = fill_words(''.join(sub_pzl), used)
            if bf:
                return bf
            else:
                used.remove(word[1])
                WORD_LOC[word[2]] = ''
                WORD_LOC[word[2] + (len(word[1]) - 1)] = ''
    return ''


make_pzl()
parse_words()
print_board(PZL)
print(PZL)
# generic_word = 'area'  # sorted(list(WORDS[4]),key=lambda x: sum([LETTER_FREQ[i] for i in x.lower()]), reverse=True)[0]
# print(generic_word)
# ind = PZL.find(SPACE)
# PZL = [*PZL]
# found = False
# for ind in range(len(PZL)):
#     if PZL[slice(ind, ind + 4 * WIDTH, WIDTH)] == [SPACE]*4:
#         for i, letter in enumerate(generic_word):
#             PZL[ind + WIDTH * i] = letter
#         break
#
# PZL = ''.join(PZL)
#
PZL = fill_words(PZL, set())
print_board(PZL)

print(list(PREFIXES[3][(0, 't')] & PREFIXES[3][(2, 'e')]))
