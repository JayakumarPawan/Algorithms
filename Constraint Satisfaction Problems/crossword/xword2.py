import sys
import re
import random
import time
sys.setrecursionlimit(10000000)
WIDTH = 3
HEIGHT = 3
N_BLOCKS = 9
SEED_STRINGS = []
DICT_FILE = 'words.txt'
BLOCK = "#"
SPACE = "-"
PZL = 9 * SPACE
LETTERS = set('abcdefghijklmnopqrstuvwxyz')

WORDS = set()  # set of all words in the dictionary
PREFIXES = {}  # dictionary binned first by length then by the position of letters that show up ex word begins with 'a'
LETTER_FREQ = {i: 0 for i in LETTERS}  # frequency of the letters in the words
CONSTRAINTS = {}  # sorted tuple of positions and list the words that can go there
POS_TO_CONSTRAINT = {}  # position and the constraints its part of
used = set()  # set of words used
WORD_VALUE = {}  # value of word based on frequency of letters in the set


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
    global used
    global WORDS
    temp = [*PZL]
    blocks = []  # these blocks have to be here so make sure they fit the rules
    for seed in SEED_STRINGS:
        h = int(re.search(r'\d*(?=x)', seed).group(0))
        w = int(re.search(r'(?<=x)\d*', seed).group(0))
        orientation = seed[0]
        letters = seed[re.search(r'(?<=x)\d*', seed).end():].lower()
        if letters in WORDS:
            used.add(letters)
        if orientation.upper() == 'H':
            for i in range(len(letters)):
                temp[h * WIDTH + w + i] = letters[i]
                if letters[i] == BLOCK:
                    blocks.append(h * WIDTH + w + i)
                    temp[rot_index_180(h * WIDTH + w + i)] = BLOCK
        if orientation.upper() == 'V':
            for i in range(len(letters)):
                temp[h * WIDTH + w + WIDTH * i] = letters[i]
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


def print_constraints(constraints):
    a = ''
    sorted_constraints = sorted(list(constraints.keys()), key=lambda x: x[0]+x[1])
    for i in sorted_constraints:
        a+= str(len(constraints[i])) +', '
    a+='\n'
    return a


def make_constraints(pzl):
    global CONSTRAINTS
    global POS_TO_CONSTRAINT
    seen_h = set()
    seen_v = set()
    for pos, sym in enumerate(pzl):
        if sym != BLOCK:
            if pos not in seen_h:
                horizontal_constraint = set()
                # right end point
                for i in range(WIDTH - pos % WIDTH):
                    if pzl[pos + i] == BLOCK:
                        break
                    horizontal_constraint.add(pos + i)
                    seen_h.add(pos + i)
                # left end point
                for i in range(pos % WIDTH, -1, -1):
                    if pzl[pos - i] == BLOCK:
                        break
                    horizontal_constraint.add(pos - i)
                    seen_h.add(pos - i)
                word_len = max(horizontal_constraint) - min(horizontal_constraint) + 1
                valid_words = set()
                for i in PREFIXES[word_len]:
                    valid_words |= PREFIXES[word_len][i]
                horizontal_constraint = tuple(sorted(list(horizontal_constraint)))
                for i in horizontal_constraint:
                    if i in POS_TO_CONSTRAINT:
                        POS_TO_CONSTRAINT[i].append((horizontal_constraint.index(i), horizontal_constraint))
                    else:
                        POS_TO_CONSTRAINT[i] = [(horizontal_constraint.index(i), horizontal_constraint)]
                    if pzl[i] in LETTERS:
                        valid_words &= PREFIXES[word_len][((i - horizontal_constraint[0]), pzl[i])]
                CONSTRAINTS[horizontal_constraint] = valid_words
            if pos not in seen_v:
                vertical_constraint = set()
                # down endpoint
                for i in range(HEIGHT - pos // WIDTH):
                    if pzl[pos + i * WIDTH] == BLOCK:
                        break
                    vertical_constraint.add(pos + i * WIDTH)
                    seen_v.add(pos + i * WIDTH)
                # up end point
                for i in range(pos // WIDTH, -1, -1):
                    if pzl[pos - i * WIDTH] == BLOCK:
                        break
                    vertical_constraint.add(pos - i * WIDTH)
                    seen_v.add(pos - i * WIDTH)
                word_len = (max(vertical_constraint) - min(vertical_constraint)) // WIDTH + 1
                valid_words = set()

                for i in PREFIXES[word_len]:
                    valid_words |= PREFIXES[word_len][i]

                vertical_constraint = tuple(sorted(list(vertical_constraint)))
                for i in vertical_constraint:
                    if i in POS_TO_CONSTRAINT:
                        POS_TO_CONSTRAINT[i].append((vertical_constraint.index(i), vertical_constraint))
                    else:
                        POS_TO_CONSTRAINT[i] = [(vertical_constraint.index(i), vertical_constraint)]
                    if pzl[i] in LETTERS:
                        valid_words &= PREFIXES[word_len][(i // WIDTH - vertical_constraint[0] // WIDTH, pzl[i])]
                CONSTRAINTS[vertical_constraint] = valid_words


def fill_rest(pzl, n_blocks):
    if n_blocks == 0:
        return pzl
    best_spots = []
    for i in range(len(pzl) // 2 + len(pzl) % 2):
        if pzl[i] != SPACE or pzl[rot_index_180(i)] != SPACE:
            continue
        space_count = 0
        if i % WIDTH == 0 or pzl[i-1] == BLOCK:
            space_count -= 50
        if i % WIDTH == WIDTH - 1 or pzl[i+1] == BLOCK:
            space_count -= 50
        if i // WIDTH == 0 or pzl[i-WIDTH] == BLOCK:
            space_count -= 50
        if i // WIDTH == HEIGHT - 1 or pzl[i+WIDTH] == BLOCK:
            space_count -= 50
        sub_pzl = [*pzl]
        sub_pzl[i] = BLOCK
        sub_pzl[rot_index_180(i)] = BLOCK
        n_blocks = N_BLOCKS - sub_pzl.count(BLOCK)
        sub_pzl, n = fill_small_gaps(sub_pzl, [i], n_blocks)

        best_spots.append((i, random.randint(0, len(pzl)) - (n_blocks - n)))
    best_spots.sort(key=lambda x: x[1], reverse=True)

    for i, space_count in best_spots:
        sub_pzl = [*pzl]
        sub_pzl[i] = BLOCK
        sub_pzl[rot_index_180(i)] = BLOCK
        n_blocks = N_BLOCKS - sub_pzl.count(BLOCK)
        sub_pzl, n = fill_small_gaps(sub_pzl, [i], n_blocks)
        if n >= 0 and len(is_connected(sub_pzl, i, [])) >= HEIGHT * WIDTH - N_BLOCKS:
            bf = fill_rest(sub_pzl, n)
            if bf:
                return bf
    return ""


def make_pzl():
    parse_cmd()
    parse_words()
    global PZL
    anchor_blocks = place_seed_strings()
    PZL = [*PZL]
    PZL, blocks_left = fill_small_gaps(PZL, anchor_blocks, N_BLOCKS)
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

    PZL = fill_rest(PZL, N_BLOCKS - PZL.count(BLOCK))
    make_constraints(PZL)


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
    global WORD_VALUE
    global LETTER_FREQ
    # words_file = open(r'C:\Users\joe\Documents\TJ 19-20\AI\CSP\crossword\words.txt', "r").read().splitlines()
    # words_file = open(r'C:\Users\joe\Documents\TJ 19-20\AI\CSP\crossword\dctEckel.txt', "r").read().splitlines()
    words_file = open(DICT_FILE, "r").read().splitlines()
    for word in words_file:
        word = word.lower()
        WORDS.add(word)
        if len(word) >= 3:
            for letter in word:
                if letter in LETTER_FREQ:
                    LETTER_FREQ[letter] += 1
                else:
                    LETTER_FREQ[letter] = 1
                    LETTERS.add(letter)

        make_prefixes(word)
    WORD_VALUE = {word: sum([LETTER_FREQ[letter] for letter in word.lower()]) for word in WORDS if len(word) >= 3}


def get_most_constrained_position(CONSTRAINTS):
    open_constraints = {k: v for k, v in CONSTRAINTS.items() if v != 'filled'}
    minc = random.sample(open_constraints.keys(), 1)[0]
    for constraint, words in open_constraints.items():
        if len(words) < len(CONSTRAINTS[minc]):
            minc = constraint
    return minc


def find_options_for_all_locations(pzl, used, CONSTRAINTS):
    """
    @param pzl: cur board
    @param used: used words
    @return: list of tuples where first element is orientation 2nd is word 3rd is position
    """
    constraint = get_most_constrained_position(CONSTRAINTS)
    # print('cur: ', constraint)
    gap = constraint[1] - constraint[0]  # should be WIDTH for vertical words and 1 for horizontal words
    restrictions = set()
    final_word_list = CONSTRAINTS[constraint]
    for pos in constraint:
        if pzl[pos] in LETTERS:
            restrictions.add((pos // gap - constraint[0] // gap, pzl[pos]))
    for restriction in restrictions:
        final_word_list &= PREFIXES[len(constraint)][restriction]
    restrictions = set()
    for word in final_word_list:
        # print('checking: ', word)
        for pos in constraint:
            # print('on position: ', pos)
            rel_pos, other_constraint = POS_TO_CONSTRAINT[pos][0] if POS_TO_CONSTRAINT[pos][0][1] != constraint else POS_TO_CONSTRAINT[pos][1]
            if CONSTRAINTS[other_constraint] == 'filled':
                continue
            # print('rel pos and other constraint: ', rel_pos, other_constraint)
            gap = constraint[1] - constraint[0]  # should be WIDTH for vertical words and 1 for horizontal words
            if (rel_pos, word[pos // gap - constraint[0] // gap]) not in PREFIXES[len(other_constraint)]:
                restrictions.add(word)
                break
            new_words = CONSTRAINTS[other_constraint] & PREFIXES[len(other_constraint)][(rel_pos, word[pos // gap - constraint[0] // gap])]
            if not new_words:
                restrictions.add(word)
                break

    final_word_list -= restrictions
    final_word_list -= used
    final_word_list = sorted(list(final_word_list), key=lambda x: WORD_VALUE[x], reverse=True)  # might be expensive
    return constraint, final_word_list


def fill_words(pzl, used, CONSTRAINTS, depth):
    if pzl.find(SPACE) == -1:
        return pzl
    #print_board(pzl)
    #print(depth, print_constraints(CONSTRAINTS))
    constraint, words = find_options_for_all_locations(pzl, used, CONSTRAINTS)


    for word in words:
        clone = {}
        for const in CONSTRAINTS:
            if CONSTRAINTS[const] == 'filled':
                clone[const] = 'filled'
            else:
                clone[const] = set(CONSTRAINTS[const])
        sub_pzl = [*pzl]
        gap = constraint[1] - constraint[0]
        for i in constraint:
            sub_pzl[i] = word[i // gap - constraint[0] // gap]
        for pos in constraint:
            # print('on position: ', pos)
            rel_pos, other_constraint = POS_TO_CONSTRAINT[pos][0] if POS_TO_CONSTRAINT[pos][0][1] != constraint else POS_TO_CONSTRAINT[pos][1]
            if clone[other_constraint] == 'filled':
                continue
            # print('rel pos and other constraint: ', rel_pos, other_constraint)
            gap = constraint[1] - constraint[0]  # should be WIDTH for vertical words and 1 for horizontal words
            clone[other_constraint] &= PREFIXES[len(other_constraint)][(rel_pos, word[pos // gap - constraint[0] // gap])]

        clone[constraint] = 'filled'
        # print(depth, print_constraints(CONSTRAINTS))
        bf = fill_words(''.join(sub_pzl), used | {word}, clone, depth+1)
        if bf:
            return bf
        # print('backtracking', depth,' see if it change from above: ', print_constraints(CONSTRAINTS))
    return ''


make_pzl()
print_board(PZL)
print(PZL)

for k, v in CONSTRAINTS.items():
    print(k, len(v))
t1 = time.time()
PZL = fill_words(PZL, set(),CONSTRAINTS, 0)
print('took this many sec: ', time.time() -t1)
print_board(PZL)


'''
Create a dict called constraints of these starting ending tuples to the words that can go in this, update this over time

Create a list of possible choices which stores tuples in the form (orientation, position, word list)
Find the most constrained open spot

for every open spot (pzl has Space token here):
    find the  endpoints using the boundary dict
    look for how many words can be placed in this area based on the size of this area and existing letters
    store this list in the list of possible choices as the tuple described above
    

sort possible choices based on the amount of words that can go here (fewer is better)
for choice in possible choices:
    sort the word list by the commonality of the word
        every word placed affects the possible choices of the words that can go into adjacent positions
        if you put the word 'constraint' in the upper left corner of the pzl then the first vertical word has to start with a 'c'
        so you go through each position the word fills and see the amount of words that goes in the constraint set in the other orientation

        update the constraints, if there is an empty one, continue to the next word
        

backtrack if no option worked

look for length of the nearest block/border this determines the length of the word that can go here
Existing letters constrain -> use set intersections on each of these possible lengths
sort these by commonality of the letters in the words/ how many words that can form by placing that letter
if none exist, back track

   
back up plan: simple frequency thing 
'''
