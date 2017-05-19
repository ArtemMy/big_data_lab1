from itertools import combinations
import csv

def parse_csv(path):
	transaction_list = []
	with open(path, 'rt') as f:
		reader = csv.reader(f, skipinitialspace=True)
		for row in reader:
			transaction_list.append(row[1:])
	return transaction_list

def all_combinations(item):
	for s in range(1, len(item)):
		for combination in combinations(item, s):
			yield frozenset(combination)

def gen_rules(itemset, support, min_conf):
	for subset in all_combinations(itemset):
		assert(len(subset) > 0)
		remain_element = itemset.difference(subset)
		assert(len(remain_element) > 0)
		confidence = float(support[itemset]) / support[subset]
		if confidence >= min_conf:
			yield subset, remain_element, confidence
