# Based on Nick Sweeting's Repo

from itertools import product


def numberofdupes(string, idx):
    """return the number of times in a row the letter at index idx is duplicated"""
    # "abccdefgh", 2  returns 1
    initial_idx = idx
    last = string[idx]
    while idx+1 < len(string) and string[idx+1] == last:
        idx += 1
    return idx-initial_idx


def variants(word):
    """get all possible variants for a word"""
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def double_variants(word):
    """get variants for the variants for a word"""
    return set(s for w in variants(word) for s in variants(w))

def reductions(word):
    """return flat option list of all possible variations of the word by removing duplicate letters"""
    word = list(word)
    # ['h','i', 'i', 'i'] becomes ['h', ['i', 'ii', 'iii']]
    for idx, l in enumerate(word):
        n = numberofdupes(word, idx)
        # if letter appears more than once in a row
        if n:
            # generate a flat list of options ('hhh' becomes ['h','hh','hhh'])
            flat_dupes = [l*(r+1) for r in range(n+1)][:3] # only take up to 3, there are no 4 letter repetitions in english
            # remove duplicate letters in original word
            for _ in range(n):
                word.pop(idx+1)
            # replace original letter with flat list
            word[idx] = flat_dupes

    # ['h',['i','ii','iii']] becomes 'hi','hii','hiii'
    for p in product(*word):
        yield ''.join(p)

def vowelswaps(word):
    """return flat option list of all possible variations of the word by swapping vowels"""
    vowels = set('aeiouy')
    word = list(word)
    # ['h','i'] becomes ['h', ['a', 'e', 'i', 'o', 'u', 'y']]
    for idx, l in enumerate(word):
        if type(l) == list:
            pass                        # dont mess with the reductions
        elif l in vowels:
            word[idx] = list(vowels)    # if l is a vowel, replace with all possible vowels

    # ['h',['i','ii','iii']] becomes 'hi','hii','hiii'
    for p in product(*word):
        yield ''.join(p)

def both(word):
    """permute all combinations of reductions and vowelswaps"""
    for reduction in reductions(word):
        for variant in vowelswaps(reduction):
            yield variant
