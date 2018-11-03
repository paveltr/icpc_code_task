from itertools import chain, combinations, groupby, permutations
import timeit
import collections
import sys
import re
import gc
from functools import reduce


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    for c in chain(*map(lambda x: combinations(iterable, x), range(0, len(iterable)+1))):
        yield c

def give_permutation(i):
    """
    Yields a permutations of a given combination
    """
    for c in permutations(i):
        yield c

def create_dict(arr):
    """
    Index based dictionary
    """
    dicty = {}
    for i, v in enumerate(arr):
        dicty[i] = v
    return dicty

def tricky_sort(a1, a2):
    """
    Sorts one array and return the second array with index-wise order
    """
    for a in zip(*sorted(zip(a1, a2), key=lambda x: (len(x), x[0]))):
        yield a

def check_complete(starts, ends, array, threshold = 2):
    """
    Checks if combination has both starts and ends
    """
    matches = 0
    for s in starts: 
        if s in array:
            matches += 1
            break
    for e in ends:
        if e in array:
            matches += 1
            break
    return matches == abs(threshold)

def check_match(pairs):
    """
    Checks if answer fits the task
    """
    return ''.join(el[0] for el in pairs) == ''.join(el[1] for el in pairs) 

def algo(a1, a2):
    """
    Checks for the first shortest match between strings
    """
    
    assert len(a1) == len(a2)

    # fast check for first sorted elements are equal
    if a1[0] == a2[0]:
        return a1[0]
    
    start_pairs = []
    end_pairs = []
    matches = [] 
    all_pairs = []
    for el1, el2 in zip(a1, a2):
        if el1[0] == el2[0]: start_pairs.append((el1, el2))
        if el1[-1] == el2[-1]: end_pairs.append((el1, el2))
        if el1 == el2: matches.append(el1)
        all_pairs.append(((el1, el2)))
    if len(start_pairs) == 0 or len(end_pairs) == 0: return 'IMPOSSIBLE'
    
    # be default we assume that there are at least than 2 possible starts and ends
    full_search = 2
    
    # but we can decrease number of permutations if there is only one pair os pissible (start; end)
    if len(start_pairs) == 1 and len(end_pairs) == 1: 
        full_search = 0
        all_pairs.remove(start_pairs[0])
        all_pairs.remove(end_pairs[0])

    if full_search == 0: 
        if start_pairs[0] == end_pairs[0]:
            return start_pairs[0][0]
        elif start_pairs[0][0] + end_pairs[0][0] == start_pairs[0][1] + end_pairs[0][1]:
            matches.append(start_pairs[0][0] + end_pairs[0][0])
        elif end_pairs[0][0] + start_pairs[0][0] == end_pairs[0][1] + start_pairs[0][1]:
             matches.append(end_pairs[0][0] + start_pairs[0][0])
        
    lookup_a1 = create_dict([el[0] for el in all_pairs])
    lookup_a2 = create_dict([el[1] for el in all_pairs])
    range_list = list(range(len(all_pairs)))
    
    del a1, a2
       
    clean_combs = []
    sorted_names = []
    
    if len(range_list) > 0:
        for i in powerset(range_list):
            if len(i) > 0 :
                if full_search == 2:
                    if check_complete(start_pairs, end_pairs, [all_pairs[index] for index in i]) and \
                            sum([len(all_pairs[index][0]) for index in i]) == sum([len(all_pairs[index][1]) for index in i]):
                        arr1_str = ''.join(lookup_a1[index] for index in i)
                        arr2_str = ''.join(lookup_a2[index] for index in i)
                        if len(arr1_str) == len(arr2_str):
                            if reduce(lambda x, y: x + y, sorted(arr1_str)) == reduce(lambda x, y: x + y, sorted(arr2_str)):
                                clean_combs.append(i)
                else:
                    clean_combs.append(i)

        if len(clean_combs) > 0:
            for i in clean_combs:
                for combination in give_permutation(i):
                    if full_search == 2:
                        if lookup_a1[combination[0]][0] != lookup_a2[combination[0]][0] or \
                            lookup_a1[combination[-1]][-1] != lookup_a2[combination[-1]][-1]:
                                continue
                        if check_match([all_pairs[index] for index in combination]):
                            matches.append(''.join(all_pairs[index][0] for index in combination))
                    elif full_search == 0:
                        option = start_pairs + [all_pairs[index] for index in combination] + end_pairs
                        if check_match(option):
                            matches.append(''.join(el[0] for el in option))
              
    if len(matches) > 0:
        matches = sorted(matches, key=lambda x: (len(x), x[0]))
        return matches[0]    
    return 'IMPOSSIBLE'
    
def string_processor(string):
    """
    Splits string by integers and returns arrays with only letters inside
    """
    arr = ' '.join(re.findall(r'[0-9|a-zA-Z]+', string.replace(r'\n', ' '))).strip()
    all_ints = re.findall(r'[0-9]+', arr)
    arr = re.compile(r'[0-9]+').split(arr)
    arr = [re.findall(r'[a-zA-Z]+', a) for a in arr if len(a) > 0]

    for r in arr:
        yield r

def substring_processor(substring, shift = 0):
    """
    Returns two array with the first and the second sequences
    """
    arr1 = []
    arr2 = []
    for i in range(0, len(substring), 2):
        yield substring[i + shift]

def string_arr(arr1, arr2):    
    for t in tricky_sort(arr1, arr2):
        yield t

def process_file(file):
    """
    Iterates over all sequences in a file
    """

    case_counter = 0

    for sub in string_processor(file):
        case_counter += 1
        str1, str2 = string_arr(substring_processor(sub), substring_processor(sub, shift = 1))
        print('Case %s: ' %  str(case_counter) + algo(str1, str2) + '\n')

def read_files():
    """
    Takes input data
    """
    input_string = ''
    for f in sys.stdin:
        input_string += f
    process_file(input_string)

read_files()