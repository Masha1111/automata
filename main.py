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


# def make_list_using_cycles(step_number, len_list):
#     result = []
#     zero_array = []
#     for i in range(step_number):
#         zero_array.append(0)
#     dec(zero_array, step_number, step_number, 0, result)
#     result = result[::-1]
#     for element in result:
#         step_decomposition = []
#         amount = 0
#         count = 0
#         for e in element:
#             if e != 0:
#                 count += 1
#         if count <= len_list:
#             for num in element:
#                 if amount + num <= step_number:
#                     amount += num
#                     step_decomposition.append(num)
#             for q in range(len_list - len(step_decomposition)):
#                 step_decomposition.append(0)
#             yield itertools.permutations((step_decomposition))

def make_list_using_cycles(step_number, len_list):
    list_using_cycles = []
    result = []
    zero_array = []
    for i in range(step_number):
        zero_array.append(0)
    dec(zero_array, step_number, step_number, 0, result)
    result = result[::-1]
    for element in result:
        temp_list = []
        step_decomposition = []
        amount = 0
        for num in element:
            if amount + num <= step_number:
                amount += num
                step_decomposition.append(num)
        for q in range(len_list - len(step_decomposition)):
            step_decomposition.append(0)
        temp_list.append([x for x in itertools.permutations(step_decomposition)])
        temp_list = list(set(temp_list[0]))
        for tup in temp_list:
            list_using_cycles.append(tup)
    list_using_cycles = list(list_using_cycles)
    list_using_cycles.sort()
    return list_using_cycles


def get_word():
    global get_automat
    global cycles
    with open("k3result.txt", 'w') as file:
        max_length_word = (len(automat) - 1) ** 2
        step = -1
        while True:
            step += 1
            list_using_cycles = make_list_using_cycles(step, len(cycles[0]))
            pathes = []
            for us_cycles in list_using_cycles:
                pathes.append(find_path(us_cycles))
            pathes.sort(key=sortyLength)

            print(pathes)

            for possible_path in pathes:
                if len(possible_path) > max_length_word:
                    sys.exit("Word does not exist")
                else:
                    possible_words = make_words(possible_path)
                    result = check(possible_words)
                    if result:

                        print(possible_path)

                        file.write(str(result))
                        sys.exit(result)


def sortyLength(inputArr):
    return len(inputArr)

# def get_word():
# "'''последняя работающая версия'''
#     global get_automat
#     global cycles
#     with open("k3result.txt", 'w') as file:
#         max_length_word = (len(automat) - 1) ** 2
#         step = -1
#         while True:
#             step += 1
#             list_using_cycles = make_list_using_cycles(step, len(cycles[0]))
#             for us_cycles in list_using_cycles:
#                 last = []
#                 # for us_cycles in generator:
#                 if us_cycles not in last:
#                     last.append(us_cycles)
#                     if len(last) > 1000:
#                         last.pop(0)
#                     possible_path = find_path(us_cycles)
#                     if len(possible_path) > max_length_word:
#                         sys.exit("Word does not exist")
#                     else:
#                         possible_words = make_words(possible_path)
#                         result = check(possible_words)
#                         if result:
#                             file.write(str(result))
#                             sys.exit(result)

# def get_word():
#     global get_automat
#     global cycles
#     max_length_word = (len(automat) - 1) ** 2
#     step = -1
#     while True:
#         step += 1
#         list_using_cycles = make_list_using_cycles(step, len(cycles[0]))
#         for generator in list_using_cycles:
#             for us_cycles in generator:
#                 possible_path = find_path(us_cycles)
#                 if len(possible_path) > max_length_word:
#                     sys.exit("Word does not exist")
#                 else:
#                     possible_words = make_words(possible_path)
#                     result = check(possible_words)
#                     if result:
#                         sys.exit(result)

# def get_word():
#     global get_automat
#     global cycles
#     max_length_word = (len(automat) - 1) ** 2
#     step = -1
#     while True:
#         step += 1
#         list_using_cycles = make_list_using_cycles(step, len(cycles[1]))
#         for us_cycles in list_using_cycles:
#             '''нафига паттерн?'''
#             possible_path = find_path(us_cycles)
#             if len(possible_path) > max_length_word:
#                 sys.exit("Word does not exist")
#             else:
#                 possible_words = make_words(possible_path)
#                 result = check(possible_words)
#                 if result:
#                     sys.exit(result)


def find_path(use_cycles):
    global automat
    global cycles
    path = []
    for last_node_number in range(len(automat) - 1, -1, -1):
        for i in range(len(use_cycles) - 1, -1, -1):
            '''добавление цикла'''
            if cycles[0][i][0] == last_node_number and use_cycles[i] > 0:
                for c in range(use_cycles[i]):
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
    with open("k3.txt") as file:
        global automat
        global cycles
        cycles1 = [(0,), (3, 2, 1), (4, 3, 2), (4,)]
        cycles2 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (9,)]
        cycles3 = [(0,), (3, 2, 1), (4, 3, 2), (5, 4), (6, 5), (8, 7, 6), (9, 8, 7), (11, 10, 9), (12, 11, 10), (12,)]
        cycles = [cycles1, cycles2, cycles3]
        get_automat(file)
        get_word()


if __name__ == "__main__":
    main()
