import sys
import itertools


def convert_base(num, to_base, from_base=10):
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]


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


def cycle_for_length_calculation(b, pat_len):
    future_num = ''
    for q in range(pat_len):
        future_num += str(b - 1)
    return int(future_num)


def calculate_lenght(len_pattern, basis):
    result = 0
    for q in range(len_pattern):
        result += basis ** q
    return result


def dec(terms, sum, k, i):
    if sum < 0:
        return
    if sum == 0:
        for j in range(0, i):
            print(terms[j])
    else:
        if sum - k >= 0:
            terms[i] = k
            dec(terms, sum - k, k, i + 1)
        if k - 1 > 0:
            dec(terms, sum, k - 1, i)
    return


def make_list_using_cycles(step_number, len_list):
    result = []
    res = []
    terms = []

    return result


def get_word():
    global get_automat
    global cycles
    max_length_word = (len(automat) - 1) ** 2
    step = -1
    max_number_pattern = calculate_lenght(len(cycles[0]), 2)
    while True:
        step += 1
        list_using_cycles = make_list_using_cycles(step, len(cycles[0]))
        for us_cycles in list_using_cycles:
             for step in range(max_number_pattern):
                pat = make_pattern_for_step(step, len(cycles[0]))
                possible_path = find_path(us_cycles, pat)
                if len(possible_path) > max_length_word:
                    sys.exit("Word does not exist")
                else:
                    possible_words = make_words(possible_path)
                    result = check(possible_words)
                    if result:
                        sys.exit(result)

# def get_word():
#     global automat
#     global cycles
#     max_length_word = (len(automat) - 1) ** 2
#     step_pattern_len = calculate_lenght(len(cycles[0]), 2)
#     for base in range(2, 9):
#         step = -1
#         for_range = calculate_lenght(len(cycles[0]), base)
#         for i in range(for_range):
#             step += 1
#             # list_using_cycles = pattern_using_cycles(step, len(cycles[0]), base)
#             list_using_cycles_for_step = make_list_using_cycles()
#             for substep in range(step_pattern_len):
#                 pat = make_pattern_for_step(substep, len(cycles[0]))
#                 possible_path = find_path(list_using_cycles, pat)
#                 if len(possible_path) > max_length_word:
#                     sys.exit("Word does not exist")
#                 else:
#                     possible_words = make_words(possible_path)
#                     result = check(possible_words)
#                     if result:
#                         sys.exit(result)


def pattern_using_cycles(step_number, lenght_pattern, base):
    hex_num = str(convert_base(step_number, base))
    pattern = []
    for i in range(lenght_pattern - len(hex_num)):
        pattern.append(0)
    for j in range(len(hex_num)):
        pattern.append(int(hex_num[j]))
    return pattern


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


def check(alist_words):
    global automat
    words = alist_words
    for node in range(len(automat) - 2):
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
    with open("k3.txt") as file:
        global automat
        global cycles
        cycles1 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (9,)]
        cycles2 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (11, 10, 9), (12, 11, 10), (12,)]
        cycles3 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (11, 10, 9), (12, 11, 10),
                   (14, 13, 12), (15, 14, 13), (15,)]
        cycles = [cycles1, cycles2, cycles3]
        get_automat(file)
        get_word()


if __name__ == "__main__":
    main()
