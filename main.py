import sys
import itertools


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
    number = str(bin(step_number)[2:])
    pattern = ''
    for j in range(len_pattern - len(number)):
        pattern += '0'
    pattern += number
    return pattern


def dec(a, summ, k, i, result):
    if summ < 0:
        return
    if summ == 0:
        ar = []
        for j in range(0, i):
            ar.append(a[j])
        result.append(ar)
    else:
        if summ - k >= 0:
            a[i] = k
            dec(a, summ - k, k, i + 1, result)
        if k - 1 > 0:
            dec(a, summ, k - 1, i, result)
    return


def make_list_using_cycles(len_use_list, len_p):
    global cyclesconf
    list_using_cycles = []
    result = []
    zero_array = []
    decomp_number = 1
    for p in range(len_p):
        for i in range(decomp_number):
            zero_array.append(0)
        dec(zero_array, decomp_number, decomp_number, 0, result)
        for sublist in result:
            if len(sublist) <= len_use_list:
                possible_using_cycle = []
                for num in sublist:
                    possible_using_cycle.append(num)
                for i in range(len_use_list - len(possible_using_cycle)):
                    possible_using_cycle.append(0)
                variants = [[x for x in itertools.permutations(possible_using_cycle)]]
                variants = list(set(variants[0]))
                for variant in variants:
                    way_len = 0
                    for j in range(len(variant)):
                        if variant[j] == 0:
                            way_len += 1
                        else:
                            way_len += cyclesconf[2][j] + 1
                    if way_len == len_p:
                        list_using_cycles.append(variant)
        decomp_number += 1
    return list_using_cycles


def get_word():
    global get_automat
    global cycles
    with open("k5result.txt", 'w') as file:
        max_length_word = (len(automat) - 1) ** 2
        len_possible_path = 4
        while True:
            len_possible_path += 1
            list_using_cycles = make_list_using_cycles(len(cycles[2]), len_possible_path)
            pathes = []
            for us_cycles in list_using_cycles:
                pathes.append(find_path(us_cycles))
            pathes.sort(key=sortyLength)
            for possible_path in pathes:
                if len(possible_path) > max_length_word:
                    sys.exit("Word does not exist")
                else:
                    possible_words = make_words(possible_path)
                    result = check(possible_words)
                    if result:
                        file.write(str(result))
                        sys.exit(result)


def sortyLength(inputArr):
    return len(inputArr)


def find_path(use_cycles):
    global automat
    global cycles
    path = []
    for last_node_number in range(len(automat) - 1, -1, -1):
        for i in range(len(use_cycles) - 1, -1, -1):
            '''добавление цикла'''
            if cycles[2][i][0] == last_node_number and use_cycles[i] > 0:
                for c in range(use_cycles[i]):
                    for node in cycles[2][i]:
                        path.append(node)
                path.append(last_node_number)

            if len(path) == 0:
                path.append(last_node_number)
            else:
                if path[-1] != last_node_number and i == 0:
                    path.append(last_node_number)
    return path


def check(alist_words):
    global automat
    words = alist_words
    for node in range(len(automat) - 1):
        answer = check_words(node, words)
        if not answer:
            return False
        words = answer
    return words


def check_words(current_n, words):
    global automat
    step_done = False
    possible_answer = []
    for word in words:
        current_node = current_n
        for i in range(len(word)):
            next_node = None
            tuples = list(automat[current_node].items())
            for tup in tuples:
                if word[i] in tup[1]:
                    next_node = tup[0]
                    step_done = True
            if next_node is not None and step_done:
                current_node = next_node
                step_done = False
            if i == len(word) - 1 and current_node == 0:
                possible_answer.append(word)
    if not possible_answer:
        return False
    else:
        return possible_answer


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
    with open("k5.txt") as file:
        global automat
        global cycles
        global cyclesconf
        cycles1 = [(0,), (3, 2, 1), (4, 3, 2), (4,)]
        cycles1conf = [1, 3, 3, 1]
        cycles2 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (9,)]
        cycles2conf = [1, 3, 3, 2, 2, 3, 3, 1]
        cycles3 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (11, 10, 9), (12, 11, 10), (12,)]
        cycles3conf = [1, 3, 3, 2, 2, 3, 3, 3, 3, 1]
        cycles = [cycles1, cycles2, cycles3]
        cyclesconf = [cycles1conf, cycles2conf, cycles3conf]
        get_automat(file)
        get_word()


if __name__ == "__main__":
    main()
