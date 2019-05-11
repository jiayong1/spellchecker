import collections
import re

import nltk
import pandas as pd
from nltk.metrics.distance import edit_distance
from tqdm import tqdm


def train(text, model):
	"""generate or update a word model (dictionary of word:frequency)"""
	words = lambda text : re.findall('[a-z]+', text.lower())
	for word in words(text):
		model[word] += 1
	return model


model = collections.defaultdict(lambda: 0)
model = train(open('data/words.txt').read(), model)
real_words = set(model)

# generate Test Dataset 

data = pd.DataFrame(columns = ["Correct", "Misspelling"])
f = open("data/misspelling.txt", "r")
j = 0

alphabet = set('abcdefghijklmnopqrstuvwxyz')
for i in tqdm(f):
	# print(j)
	# if j > 50:
	# 	break
	j += 1
	if i[0] =="$":
		correct = i[1:].lower().strip()
	else:
		i = i.lower().strip()
		if not (i in real_words) and not (set(i) - alphabet) and not (set(correct) - alphabet) and 0 < edit_distance(correct, i) <= 2:
			data = data.append({'Correct': correct, 'Misspelling':i},ignore_index=True)

data.to_csv( path_or_buf = 'data/testdata.txt' ,sep=' ', index=False, header=False )
