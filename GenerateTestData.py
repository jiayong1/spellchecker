import pandas as pd
import nltk
from tqdm import tqdm
from nltk.metrics.distance import edit_distance

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
		if not (set(i.lower().strip()) - alphabet) and edit_distance(correct, i.lower().strip()) <= 2:
			data = data.append({'Correct': correct, 'Misspelling':i.lower().strip()},ignore_index=True)

data.to_csv( path_or_buf = 'data/testdata.txt' ,sep=' ', index=False, header=False )
	




