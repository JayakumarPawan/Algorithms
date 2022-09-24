import sys
import re

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
LETTER_FREQ = { i : 0 for i in 'abcdefghijklmnopqrstuvwxyz'}
WORD_LOC = [''] * 9


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
                if i == len(letters) -1:
                    WORD_LOC[h * WIDTH + w + i] = 'e'
                if letters[i] == BLOCK:
                    blocks.append(h * WIDTH + w + i)
                    temp[rot_index_180(h * WIDTH + w + i)] = BLOCK
                # else:
                    # if h == 0:
                    #     if temp[h * WIDTH + w + i + WIDTH] == SPACE:
                    #         temp[h * WIDTH + w + i + WIDTH] = '*'
                    #     if temp[h * WIDTH + w + i + 2 * WIDTH] == SPACE:
                    #         temp[h * WIDTH + w + i + 2 * WIDTH] = '*'
                    # if h == HEIGHT - 1:
                    #     if temp[h * WIDTH + w + i - WIDTH] == SPACE:
                    #         temp[h * WIDTH + w + i - WIDTH] = '*'
                    #     if temp[h * WIDTH + w + i - 2 * WIDTH] == SPACE:
                    #         temp[h * WIDTH + w + i - 2 * WIDTH] = '*'
                    # else:
                    #     if temp[h * WIDTH + w + i - WIDTH] == SPACE:
                    #         temp[h * WIDTH + w + i - WIDTH] = '*'
                    #     if temp[h * WIDTH + w + i + WIDTH] == SPACE:
                    #         temp[h * WIDTH + w + i + WIDTH] = '*'
        if orientation.upper() == 'V':
            for i in range(len(letters)):
                temp[h * WIDTH + w + WIDTH * i] = letters[i]
                if i == 0:
                    WORD_LOC[h * WIDTH + w] = 's'
                if i == len(letters) -1:
                    WORD_LOC[h * WIDTH + w + WIDTH * i] = 'e'
                if letters[i] == BLOCK:
                    blocks.append(h * WIDTH + w + WIDTH * i)
                    temp[rot_index_180(h * WIDTH + w + WIDTH * i)] = BLOCK
                # else:
                    # if w == 0:
                    #     if temp[h * WIDTH + w + WIDTH * i+ 1] == SPACE:
                    #         temp[h * WIDTH + w + WIDTH * i+ 1] = '*'
                    #     if temp[h * WIDTH + w + WIDTH * i + 2] == SPACE:
                    #         temp[h * WIDTH + w + WIDTH * i + 2] = '*'
                    # if w == WIDTH - 1:
                    #     if temp[h * WIDTH + w + WIDTH * i - 1] == SPACE:
                    #         temp[h * WIDTH + w + WIDTH * i - 1] = '*'
                    #     if temp[h * WIDTH + w + WIDTH * i - 2] == SPACE:
                    #         temp[h * WIDTH + w + WIDTH * i - 2] = '*'
                    # else:
                    #     if temp[h * WIDTH + w + WIDTH * i - 1] == SPACE:
                    #         temp[h * WIDTH + w + WIDTH * i - 1] = '*'
                    #     if temp[h * WIDTH + w + WIDTH * i + 1] == SPACE:
                    #         temp[h * WIDTH + w + WIDTH * i + 1] = '*'

    PZL = ''.join(temp)
    return blocks


def fill_small_gaps(pzl, anchors, n_blocks):
    temp = [*pzl]
    # This takes care of making sure there is enough space between blocks and borders
    for i in anchors:
        #print_board(temp)
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
    if n_blocks == 0:
        return pzl
    for i in range(len(pzl) // 2 + len(pzl) % 2):
        if pzl[i] != SPACE or pzl[rot_index_180(i)] != SPACE:
            continue
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


def parse_words():
    global WORDS
    global PREFIXES
    WORDS = {}  # = { 'a' : {5: ['apple'], 3:['and','app']}} words in the list are sorted by commonality of letters
    PREFIXES = {}
    global LETTER_FREQ
    #print(letter_frequency)
    words_file = open('words.txt', "r").read().splitlines()
    # words_file = open(r'C:\Users\joe\Documents\TJ 19-20\AI\words.txt', "r").read().splitlines()
    for word in words_file:
        if len(word) < 3:
            continue
        if len(word) not in WORDS:
            WORDS[len(word)] = set()
        for letter in word:
            LETTER_FREQ[letter] += 1
        if word[0] not in WORDS:
            WORDS[word[0]] = {}
        if word[:2] not in WORDS:
            WORDS[word[:2]] = {}
        if word[:3] not in WORDS:
            WORDS[word[:3]] = {}
        if len(word) not in WORDS[word[0]]:
            WORDS[word[0]][len(word)] = set()
        if len(word) not in WORDS[word[:2]]:
            WORDS[word[:2]][len(word)] = set()
        if len(word) not in WORDS[word[:3]]:
            WORDS[word[:3]][len(word)] = set()
        WORDS[word[0]][len(word)].add(word)
        WORDS[word[:2]][len(word)].add(word)
        WORDS[word[:3]][len(word)].add(word)
        WORDS[len(word)].add(word)
        for i in range(len(word)):
            if word[:i] in PREFIXES:
                PREFIXES[word[:i]].add(word)
            else:
                PREFIXES[word[:i]] = {word}

    # print(letter_frequency)

    # print(WORDS)


def find_options_for_all_locations(pzl, used):
    final_options = []  # pos: list of tuples where first element is orientation 2nd is word 3rd is position
    for position in range(len(pzl)):
        pos_options = []
        w_h = True  # possible to put a word horizontally
        w_v = True  # possible for vertical
        if pzl[position] == BLOCK:
            continue

        # find the closest obstacle in right or down (border or block):
        block_pos = pzl.find(BLOCK,position)
        if block_pos != -1:
            max_len_H = min(block_pos,position - position % WIDTH + WIDTH) - position
        else: # no block so just right
            max_len_H = WIDTH - position % WIDTH

        vertical_slice = pzl[slice(position,len(pzl), WIDTH)]
        block_pos = vertical_slice.find(BLOCK)
        if block_pos != -1:
            max_len_V = min(position + vertical_slice.find(BLOCK) * WIDTH, 1 + position + WIDTH * (HEIGHT - position//WIDTH - 1)) // WIDTH - position //WIDTH
        else:  # no block so just bottom
            max_len_V = HEIGHT - position // WIDTH

        if max_len_V < 3 or SPACE not in vertical_slice:
            w_v = False
        if max_len_H < 3 or SPACE not in pzl[position: position+max_len_H]:
            w_h = False
        if not (w_h or w_v):
            continue

        # create tokens:
        if w_h:
            # find the first open spot in the range(position: closest obstacle):
            open_spot_H = pzl.find(SPACE, position)
            token_H = pzl[position:open_spot_H]
            if len(token_H) > 3 or token_H not in WORDS:
                w_h = False
        if w_v:
            # find the first open spot in the range(position: closest obstacle):
            open_spot_V = vertical_slice.find(SPACE) * WIDTH + position
            token_V = pzl[slice(position, open_spot_V, WIDTH)]
            if len(token_V) > 3 or token_V not in WORDS:
                w_v = False
        if not (w_h or w_v):
            continue

        # options = all words that start with token and are small enough:
        if w_h:
            options_h = set()
            if token_H == '':
                for i in range(3, max_len_V+1):
                    options_h |= WORDS[i]
            else:
                for i, wrds in WORDS[token_H].items():
                    if i <= max_len_H:
                        options_h |= wrds
            options_h -= used
            # ensure word matches prefix of some un-used word if so add to final options
            for word in options_h:
                use = True
                word_loc = ''.join(WORD_LOC)
                for i, letter in enumerate(word):
                    # check the spot the puzzle is actually filling in
                    if not (pzl[position + i] == letter or pzl[position + i] == SPACE):
                        use = False
                        break
                    '''
                    # find the prefix of the word affected by the letter
                    vertical_slice = word_loc[slice((position + i) % WIDTH, position + i, WIDTH)]
                    word_start = vertical_slice.rfind('s')
                    word_end = vertical_slice.rfind('e')
                    prefix_start = position
                    if word_end > word_start:
                        prefix_start = word_end + 1
                    if word_start > word_end:
                        prefix_start = word_start
                    word_prefix = pzl[prefix_start: position]
                    if len(word_prefix) > 0:
                        use = False
                        for prefix in PREFIXES:
                            if len(PREFIXES[prefix]) == 0:
                                continue
                            # prefixes match
                            match = True
                            for j, ltr in enumerate(word_prefix):
                                if ltr == SPACE:
                                    continue
                                if ltr != prefix[j]:
                                    match = False
                                    break
                            if match:
                                use = True
                                break
                    # check the spot the puzzle is actually filling in
                    if not(pzl[position + i] == letter or pzl[position + i] == SPACE):
                        use = False
                if use:
                    pos_options.append(('H', word, position))
                '''
        if w_v:
            options_v = set()
            if token_V == '':
                for i in range(3, max_len_V+1):
                    options_v |= WORDS[i]
            else:
                for i, wrds in WORDS[token_V].items():
                    if i <= max_len_V:
                        options_v |= wrds
            options_v -= used
            # ensure word matches existing stuff if so add to final options
            for word in options_v:
                use = True
                for i, letter in enumerate(word):
                    # check if the word is attempting to override existing letters
                    if not(pzl[position + WIDTH * i] == letter or pzl[position + WIDTH * i] == SPACE):
                        use = False
                        break
                    '''
                    # find the prefix of the word affected by the letter
                    word_start = word_loc.rfind('sh', position + i * WIDTH - position % WIDTH, position + i * WIDTH)

                    # find the beginning pos of the horizontal words affected by this letter
                    frag_start = position
                    for j in range(position % WIDTH - 1,-1,-1):
                        if 'eh' in WORD_LOC[position + WIDTH * i - j]:
                            frag_start = position + WIDTH * i - j
                    if frag_start == -1:
                        frag_start = position

                    # find the end pos of the horizontal words affected by this letter
                    for j in range(position,WIDTH-1):
                        if


                    word_end = word_loc.rfind('e', position + i * WIDTH - position % WIDTH, position + i * WIDTH)
                    prefix_start = position
                    if word_end > word_start:
                        prefix_start = word_end + 1
                    if word_start > word_end:
                        prefix_start = word_start
                    word_prefix = pzl[prefix_start: position+1]
                    # if the prefix isnt there because first word or end of word is right next to position then its fine
                    # if the prefix is there then you have to make sure a word can actually be formed by it
                    if len(word_prefix) > 0:
                        use = False
                        for prefix in PREFIXES:
                            if len(PREFIXES[prefix]) == 0:
                                continue
                            # prefixes match
                            match = True
                            for j, ltr in enumerate(word_prefix):
                                if ltr == SPACE:
                                    continue
                                if ltr != prefix[j]:
                                    match = False
                                    break
                            if match:
                                use = True
                                break
                    if not use:
                        break
                if use:
                    pos_options.append(('V', word, position))
                '''

        # sort words based on freq of letters (sum([frequency(letter) for letter in word]))
        pos_options.sort(key=lambda x: sum([LETTER_FREQ[i] for i in x[1]]))
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
            if word[0] == 'H':
                for i, letter in enumerate(word[1]):
                    if i == 0:
                        WORD_LOC[word[2]] += 'sh'
                    if i == len(word[1]) - 1:
                        WORD_LOC[word[2] + i] += 'eh'

                    if word[1][:i] in PREFIXES:
                        PREFIXES[word[1][:i]].remove(word[1])

                    sub_pzl[word[2]+i] = letter
            else:
                for i, letter in enumerate(word[1]):
                    if i == 0:
                        WORD_LOC[word[2]] += 'sv'
                    if i == len(word[1]) - 1:
                        WORD_LOC[word[2] + i * WIDTH] += 'ev'

                    if word[1][:i] in PREFIXES:
                        PREFIXES[word[1][:i]].remove(word[1])

                    sub_pzl[word[2] + i * WIDTH] = letter

            used.add(word[1])
            bf = fill_words(''.join(sub_pzl), used)
            if bf:
                return bf
            else:
                used.remove(word[1])
                WORD_LOC[word[2]] = WORD_LOC[word[2]][:-2]
                WORD_LOC[word[2] + len(word[1]) - 1] = WORD_LOC[word[2] + len(word[1]) - 1][:-2]
                for i in range(len(word[1])):
                    PREFIXES[word[1][:i]].add(word[1])
    return ''


make_pzl()
parse_words()
ind = PZL.find('---')

PZL = [*PZL]
PZL[ind] = 's'
PZL[ind+1] = 'e'
PZL[ind+2] = 'a'
ind = PZL.rfind('---')
PZL[ind] = 't'
PZL[ind+1] = 'e'
PZL[ind+2] = 'a'
PZL = ''.join(PZL)
PZL = fill_words(PZL, set())
print_board(PZL)

