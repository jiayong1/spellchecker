# Evaluation code for the spell checker

import pickle
import os
import pdb

def merge_test_dataset(datasets):
	"""
	Merge multiple datasets into one dict.
	"""
	if len(datasets) == 1:
		return datasets[0]
	else:
		for i in range(1, len(datasets)):
			datasets[0].update(datasets[i])
		return datasets[0]

def load_test_dataset(root, dataset_names):
	"""
	Dataset structure is currently a pickled dict of (misspelled: ground truth).
	"""
	sets = []
	for one in dataset_names:
		dataset_path = os.path.join(root, one)
		if not os.path.exists(dataset_path):
			print("%s doesn't exist!" %dataset_path)
			return None
		with open(dataset_path) as f:
			testset_this = pickle.load(f)
		sets.append(testset_this)
	testset = merge_test_dataset(sets)
	return testset


def evaluate(test_dataset):
	"""
	Evaluate and calculate the precision.
	"""
	correct = 0
	for word in test_dataset:
		### TODO
#		output = predict(word)
#		if output == test_dataset[word]:
#			correct += 1
		pass

	print("===========================================")
	print("Precision: %.4f of %d misspelled words." %(float(correct) / len(test_dataset), len(test_dataset)))
	print("===========================================")


def main():
	root = "./data/testset"
	# Please refer to https://www.dcs.bbk.ac.uk/~ROGER/corpora.html for the info of the datasets
	# there are more on this page
	test_dataset_names = ['birkbeck.pkl', 'holbrook.pkl']
	test_dataset = load_test_dataset(root, test_dataset_names)
	if test_dataset != None:
		evaluate(test_dataset)


if __name__ == '__main__':
	main()