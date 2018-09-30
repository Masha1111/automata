def get_automat(data):
    count = int(data.readline())
    global automat
    automat = [{} for i in range(count)]
    lines = data.read().split('\n')
    for i in range(len(lines)):
        split_strings = lines[i].split()
        keys = automat[int(split_strings[0])].keys()
        if int(split_strings[1]) in keys:
            automat[int(split_strings[0])][int(split_strings[1])] += split_strings[2]
        else:
            automat[int(split_strings[0])][int(split_strings[1])] = split_strings[2]


def make_pattern_for_step(step_number, len_pattern):
    for i in range(1, 2 ** len_pattern):
        number = bin(step_number)[2:]
        pattern = ''
        for j in range(len_pattern - len(number)):
            pattern += '0'
        pattern += number
    return pattern


def get_word():
    global automat
    global cycles
    max_length_word = (len(automat) - 1) ** 2
    # for i in range(max_length_word - len(automat)):
    #     path = find_path(i, cycles)
    #     possible_words = make_words(path)
    #     check_words(possible_words, path)
    for i in range(max_length_word - len(automat)):
        list_using_cycles = [0, 0, 0, 0, 0, 0, 0, 0]
        for k in range(len(cycles[0])):
            pat = make_pattern_for_step(0, len(cycles[0]))
            possible_path = find_path(list_using_cycles, pat)
            possible_words = make_words(possible_path)
            result = check(possible_words)


def make_list_using_cycles():
    pass


def find_path(use_cycles, pattern):
    """pattern в двоичном виде для одного шага
    use_cycles: [0, 2, ...], где element - количество пробегов по циклу
    cycles1 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (9,)]"""
    global automat
    global cycles
    path = []
    using = []
    for j in range(len(pattern)):
        using.append(int(pattern[j]) + use_cycles[j])
    for last_node_number in range(len(automat) - 1, -1, -1):
        for i in range(len(using) - 1, -1, -1):
            '''добавление цикла'''
            if cycles[0][i][0] == last_node_number and using[i] > 0:
                for c in range(using[i]):
                    for node in cycles[0][i]:
                        path.append(node)
                path.append(last_node_number)

            if len(path) == 0:
                path.append(last_node_number)
            else:
                if path[-1] != last_node_number and i == 0:
                    path.append(last_node_number)
    return path


def check(words):
    global automat
    for node in range(len(automat) - 2):
        answer = check_words(node, words)
        if not answer:
            return False
    return True


def check_words(current_n, words):
    global automat
    current_node = current_n
    step_done = False
    for word in words:
        for letter in word:
            next_node = None
            tuples = list(automat[current_node].items())
            for tup in tuples:
                if letter in tup[1]:
                    next_node = tup[0]
                    step_done = True
            if next_node is not None and step_done:
                current_node = next_node
                step_done = False
            else:
                return False
    if current_node != 0:
        return False
    return True


def make_list_cycles(length):
    pattern = []
    for i in range(length):
        pattern.append((0, False))
    return pattern


def make_words(path):
    global automat
    words = []
    word = ''
    index = 0
    change = dict()
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node_number = path[i + 1]
        value = automat[current_node][next_node_number]
        letters = []
        for val in value:
            for letter in val:
                letters += letter
        if len(letters) > 1:
            change[index] = letters[1]
        word += letters[0]
        index += 1
    words.append(word)
    search_words(change, words)
    return words


def search_words(list_changes, words):
    original = words[0]
    changes = list(list_changes.items())
    keys = list(list_changes.keys())
    length = len(changes)
    for i in range(1, 2 ** length):
        copy = ''
        pattern = make_pattern_for_step(i, length)
        index_list = []
        for q in range(len(pattern)):
            if pattern[q] == '1':
                index_list.append(q)
        for k in range(len(original)):
            if k not in keys:
                copy += original[k]
            else:
                for index in index_list:
                    if changes[index][0] == k:
                        copy += changes[index][1]
                if len(copy) - 1 < k:
                    copy += original[k]
        words.append(copy)


def main():
    with open("k3.txt") as file:
        global automat
        global cycles
        cycles1 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (9,)]
        cycles2 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (11, 10, 9), (12, 11, 10), (12,)]
        cycles3 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (11, 10, 9), (12, 11, 10),
                   (14, 13, 12), (15, 14, 13), (15,)]
        cycles = [cycles1, cycles2, cycles3]
        get_automat(file)
        # path = find_path([0, 0, 0, 0, 0, 0, 0, 0], '00000000')
        # words = make_words(path)
        # print(words)
        check_words(['aababaaba', 'aabababba', 'abbabaaba', 'abbababba'])
        # print(automat)
        # get_word()


if __name__ == "__main__":
    main()
