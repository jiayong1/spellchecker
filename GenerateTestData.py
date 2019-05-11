import pandas as pd

# generate Test Dataset 

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




data = pd.DataFrame(columns = ["Correct", "Misspelling"])
f = open("data/misspelling.txt", "r")
j = 0

alphabet = set('abcdefghijklmnopqrstuvwxyz')
for i in f:
	print(j)
	#if j > 50:
	#	break
	j += 1
	if i[0] =="$":
		correct = i[1:].lower().strip()
	else:
		if not (set(i.lower().strip()) - alphabet) and correct in double_variants(i.lower().strip()):
			data = data.append({'Correct': correct, 'Misspelling':i.lower().strip()},ignore_index=True)

data.to_csv( path_or_buf = '/Users/jiayonglin/Desktop/701_spellchecker/data/testdata.txt' ,sep=' ', index=False, header=False )
	




