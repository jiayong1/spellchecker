# Created by Hanyu Wang

import numpy as np
from spellchecker import give_suggestions


def load_score_mat(path='scorematrix.npy'):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    mat = np.load(path)

    assert mat.shape == (26, 26)

    score = {}
    for i in range(26):
        for j in range(26):
            score[alphabet[i], alphabet[j]] = mat[i, j]

    return score


def align(a:str, b:str, sigma:int, score:dict) -> int:

    len_a, len_b = len(a), len(b)
    end = (len_a, len_b)
    pool = {}
    pool[0, 0] = (0, (-1, -1))

    for i in range(1, len_a+1):
        pool[i, 0] = (-sigma*i, (i-1, 0))

    for i in range(1, len_b+1):
        pool[0, i] = (-sigma*i, (0, i-1))

    for idx_a in range(1, len_a+1):
        for idx_b in range(1, len_b+1):
            candidates = []
            candidates.append((pool[idx_a-1, idx_b][0] - sigma, (idx_a-1, idx_b)))
            candidates.append((pool[idx_a, idx_b-1][0] - sigma, (idx_a, idx_b-1)))
            candidates.append((pool[idx_a-1, idx_b-1][0] + score[a[idx_a-1], b[idx_b-1]], (idx_a-1, idx_b-1)))                
            pool[idx_a, idx_b] = max(candidates, key=lambda x : x[0])
    
    return pool[end][0]

def final_suggestions(word:str, sug:set, score, topk=3, sigma=5) -> list:
    candidates = [(p_word, align(word, p_word, sigma=sigma, score=score)) for p_word in sug]
    return sorted(candidates, key=lambda x: x[1], reverse=True)[:topk]


def backtrace(pool:dict, a, b):
    len_a, len_b = len(a), len(b)
    l_a, l_b = list(a), list(b)
    end = (len_a, len_b)
    act_a = []
    act_b = []

    now = end
    while True:
        pre = pool[now][1]
        if pre[0] < 0:
            break
        if pre[0] == now[0]:
            act_a.append('-')
        else:
            act_a.append(l_a.pop())
        if pre[1] == now[1]:
            act_b.append('-')
        else:
            act_b.append(l_b.pop()) 
        now = pre 

    return str(pool[end][0]), ''.join(reversed(act_a)), ''.join(reversed(act_b))     


if __name__ == "__main__":
    score = load_score_mat()
    while True:
        word = str(input('>'))
        sug = give_suggestions(word, False)
        fs = final_suggestions(word, sug, score, topk=10, sigma=5)
        print(fs)

