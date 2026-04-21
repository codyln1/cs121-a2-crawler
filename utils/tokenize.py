# Note: adapted from Caden Lee's Assigment 1 (as I am one of the group members)
from functools import cmp_to_key
from text import is_stop_word

def is_valid_token_char(c):
    return c.isalnum() and c.isascii()

def is_token_continuer(c):
    # Need this to turn separate words like "we're" into "were"
    # while ignoring quotes around words like "'example'"
    return c == "'"

def split_alnum(line):
    curr = ''
    for c in line:
        # Check for English alphanumeric characters only
        if is_valid_token_char(c):
            curr += c
        elif is_token_continuer(c):
            continue
        else:
            if (len(curr) > 0):
                yield curr
            curr = ''
    if (len(curr) > 0):
        yield curr

def computeWordFrequencies(tokens):
    res = {}

    for tok in tokens:
        if (tok in res):
            res[tok] += 1
        else:
            res[tok] = 1

    return res

def compareTokenEntries(item1, item2):
    if item1[1] > item2[1]:
        return -1
    elif item1[1] < item2[1]:
        return 1
    elif item1[0] < item2[0]:
        return -1
    else:
        return 1

# Returns a sorted dictionary of valid tokens and their frequencies
# Stop words are removed
# Currently altered so that the return is the unsorted version of dictionary
def tokenize(input_string):
    tokens = []

    for line in input_string.splitlines():
        for word in split_alnum(line):
            tok = word.lower()
            if is_stop_word(tok):
                continue
            tokens.append(tok)

    freq = computeWordFrequencies(tokens)

    #sorted_freq = dict(sorted(freq.items(), key=cmp_to_key(compareTokenEntries)))

    return freq

# Takes an existing dictionary, tokenizes an input string and merges the two together
def merge_with_input(existing_dict, input_string):
    new_merge = tokenize(input_string)
    for key, value in new_merge.items():
        if key in existing_dict:
            existing_dict[key] += value
        else:
            existing_dict[key] = value

    return existing_dict
