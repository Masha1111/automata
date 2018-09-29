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
    cycles = make_list_cycles(len(automat))
    max_length = (len(automat) - 1) ** 2
    for i in range(max_length - len(automat)):
        path = find_path(i, cycles)
        possible_words = make_words(path)
        check_words(possible_words, path)


def find_path(use_cycles, pattern):
    """pattern в двоичном виде для одного шага
    use_cycles: [0, 2, ...], где element - количество пробегов по циклу
    cycles1 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (9,)]"""
    global automat
    global cycles
    last_node = automat[-1]
    last_node_number = len(automat) - 1
    path = []
    using = []
    for j in range(len(pattern)):
        using.append(int(pattern[j]) + use_cycles[j])
    for k in range(len(automat)):
        for i in range(len(using) - 1, 0, -1):
            if cycles[0][i][0] == last_node_number and using[i] > 0:
                for c in range(using[i]):
                    for node in cycles[0][i]:
                        path.append(node)
                        path.append(last_node_number)
                path.append(list(last_node.keys())[0])
                last_node = automat[list(automat[last_node_number].keys())[0]]
                last_node_number = list(automat[last_node_number].keys())[0]
            else:
                path.append(last_node_number)
                last_node = automat[list(automat[last_node_number].keys())[0]]
                last_node_number = list(automat[last_node_number].keys())[0]
            if last_node_number == 0 and last_node_number in path:
                break
        break
    # while True:
    #     for i in range(len(using)):
    #         if cycles[0][i][0] == last_node_number and using[i] > 0:
    #             for c in range(using[i]):
    #                 for node in cycles[0][i]:
    #                     path.append(node)
    #                     path.append(last_node_number)
    #             path.append(list(last_node.keys())[0])
    #             last_node = automat[list(automat[last_node_number].keys())[0]]
    #             last_node_number = list(automat[last_node_number].keys())[0]
    #         else:
    #             path.append(last_node_number)
    #             last_node = automat[list(automat[last_node_number].keys())[0]]
    #             last_node_number = list(automat[last_node_number].keys())[0]
    #         if last_node_number == 0 and last_node_number in path:
    #             break
    #     break
    return path


def check_words(words, path):
    global automat
    for word in words:
        for node in range(len(automat) - 2, 1, -1):
            current_node = node
            next_node = None
            for letter in word:
                tuples = list(automat[current_node].items())
                for tup in tuples:
                    if tup[1] == letter:
                        next_node = tup[0]
                if next_node is not None:
                    current_node = next_node
                else:
                    break


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
        for value in value:
            for letter in value:
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
        a = automat
        res = find_path([0, 0, 0, 0, 0, 0, 0, 0], '00000000')
        print(res)
        #get_word()


if __name__ == "__main__":
    main()
