# Note: adapted from Caden Lee's Assigment 1 (as I am one of the group members)

def split_alnum(line):
    curr = ''
    for c in line:
        # Check for English alphanumeric characters only
        if c.isalnum() and c.isascii():
            curr += c
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

# Returns a sorted dictionary of valid tokens and their frequencies. These INCLUDE stopwords.
def tokenize(input_string):
    tokens = []

    for line in input_string.splitlines():
        for word in split_alnum(line):
            tok = word.lower()
            res.append(tok)

    freq = computeWordFrequencies(non_stop_words)

    sorted_freq = dict(sorted(freq.items(), key=cmp_to_key(compareTokenEntries)))

    return sorted_freq
