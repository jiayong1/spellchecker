# Author: Hanyu Wang
# The Global Anigner class, provided Global Alignment using Needleman-Wunsch algorithm.

import collections
import os

import numpy as np

from score_matrix_generator import generate_score_matrix


# the Aligner class
class Aligner:
    def __init__(self, sigma=5, bayes=True, onlyBayes=False):
        self.sigma = sigma
        self.onlyBayes = onlyBayes
        self.score = None
        self.freq_dict = None

        # load score matrix, if it does not exist, generate it from data
        path='scorematrix.npy'
        if not os.path.isfile(path):
            generate_score_matrix('data/misspelling.txt')
        self.load_score_mat(path)

        if bayes:
            self.load_freq_dict()
    
    # score matrix loading function
    def load_score_mat(self, path='scorematrix.npy'):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        mat = np.load(path)
        assert mat.shape == (26, 26)
        
        score = {}
        for i in range(26):
            for j in range(26):
                score[alphabet[i], alphabet[j]] = mat[i, j]

        self.score = score

    # load the word frequency dictionary        
    def load_freq_dict(self, path='data/frequency_dictionary_en_82_765.txt'):
        # https://github.com/wolfgarbe/SymSpell/blob/master/SymSpell/frequency_dictionary_en_82_765.txt
        freq_dict = {}
        with open(path, 'r') as f:
            for line in f:
                word, num = line.strip('\ufeff \n').split()
                # freq_dict[word] = int(num)
                freq_dict[word] = np.log(int(num))


        mean_freq = int(sum(freq_dict.values())/len(freq_dict))
        freq_dfdict = collections.defaultdict(lambda: mean_freq)
        freq_dfdict.update(freq_dict)
        self.freq_dict = freq_dfdict

    # global alignment algorithm
    def align(self, a:str, b:str) -> int:
        sigma, score = self.sigma, self.score

        a, b = a.lower(), b.lower()
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

    # give topk final suggestions using global alignment and optional Bayes Re-weighting
    def final_suggestions(self, word:str, sug:set, topk=3) -> list:
        freq_dict = self.freq_dict

        if not self.onlyBayes:
            candidates = [(p_word, self.align(word, p_word)) for p_word in sug]
            # if freq_dict is None, do not apply Bayes Re-weighting
            if freq_dict is not None:
                freq_sum = sum(freq_dict[x[0]] for x in candidates)
                candidates = [(x[0], x[1]*(freq_dict[x[0]]/freq_sum)) for x in candidates]

        # if self.onlyBayes only apply Bayes Re-weighting
        else:
            freq_sum = sum(freq_dict[p_word] for p_word in sug)
            candidates = [(p_word, freq_dict[p_word]/freq_sum) for p_word in sug]

        return sorted(candidates, key=lambda x: x[1], reverse=True)[:topk]


if __name__ == "__main__":
    from checker_backend import SpellChecker
    sc = SpellChecker(Aligner())
    # a = Aligner()
    while True:
        word = str(input('> '))
        fs = sc.give_suggestions(word, topk=10)
        print(fs)
