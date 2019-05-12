# Based on Nick Sweeting's Repo
# Authors: Hengduo Li, Hanyu Wang

import collections
import os
import pdb
import re

from functional import both, double_variants, reductions, variants, vowelswaps


class SpellChecker:
    def __init__(self, aligner, model=None):
        self.aligner = aligner
        self.model = collections.defaultdict(lambda: 0) if model is None else model
        self.train(open('data/words.txt').read())
        self.train_from_files(['./data/sherlockholmes.txt', './data/lemmas.txt', ])
        self.real_words = set(self.model)

    def train(self, text):
        # generate or update a word model (dictionary of word:frequency)
        words = lambda text : re.findall('[a-z]+', text.lower())
        for word in words(text):
            self.model[word] += 1

    def train_from_files(self, file_list):
        for f in file_list:
            self.train(open(f).read())

    # generate suggestions
    def suggestions(self, word, short_circuit=False):
        # return on first match if short_circuit is true, otherwise collect all possible suggestions
        real_words = self.real_words
        word = word.lower()
        if short_circuit:   
            return ({word}                      & real_words or   #  caps     "inSIDE" => "inside"
                    set(reductions(word))       & real_words or   #  repeats  "jjoobbb" => "job"
                    set(vowelswaps(word))       & real_words or   #  vowels   "weke" => "wake"
                    set(variants(word))         & real_words or   #  other    "nonster" => "monster"
                    set(both(word))             & real_words or   #  both     "CUNsperrICY" => "conspiracy"
                    set(double_variants(word))  & real_words or   #  other    "nmnster" => "manster"
                    {})
        else:
            return ({word}                      & real_words or
                    (set(reductions(word))  | set(vowelswaps(word)) | set(variants(word)) | set(both(word)) | set(double_variants(word))) & real_words or
                    {})

    def give_suggestions(self, word:str, topk=3):
        sug = self.suggestions(word)
        if sug: 
            return self.aligner.final_suggestions(word, sug, topk=topk)
        else:
            return None


if __name__ == "__main__":
    from align import Aligner
    sc = SpellChecker(Aligner())
    while True:
        word = str(input('>'))
        fs = sc.give_suggestions(word, topk=10)
        print(fs)
