#!/usr/bin/python3

import sys
from common import gen_rules, parse_csv
from collections import defaultdict

def get_items(dataset):
	items = set()
	transactions = list()
	for row in dataset:
		for item in row:
			if item:
				items.add(frozenset([item]))
	return items

def min_support_items(itemset, dataset, min_support, freq_dict):
	local_freq_dict = defaultdict(int)

	for item in itemset:
		if item in local_freq_dict:
			continue
		for transaction in dataset:
			if item.issubset(transaction):
				freq_dict[item] += 1
				local_freq_dict[item] += 1

	def is_supported(count):
		return float(count) / len(dataset) >= min_support

	return {i for i, c in local_freq_dict.items() if is_supported(c)}

def gen_candidates(k_itemset, k):
	if(len(k_itemset) == 0):
		return set()
	return set(filter(lambda x: len(x) == k, (frozenset(i.union(j)) for i in k_itemset for j in k_itemset)))

def k_item_set(dataset, min_support, freq_dict):
	itemset = get_items(dataset)
	k_itemset = min_support_items(itemset, dataset, min_support, freq_dict)
	k = 2
	while k_itemset != set():
		yield k_itemset
		candidates = gen_candidates(k_itemset, k)
		k_itemset = min_support_items(candidates, dataset, min_support, freq_dict)
		k += 1

def all_combinations(item):
    for s in range(1, len(item)):
    	for combination in combinations(item, s):
    		yield frozenset(combination)

def apriori(dataset, min_support, min_conf):
	freq_dict = defaultdict(int)
	item_sets = k_item_set(dataset, min_support, freq_dict)
	for k_set in item_sets:
		for itemset in k_set:
			yield from gen_rules(itemset, freq_dict, min_conf)

if __name__ == "__main__":
	if(len(sys.argv) < 4):
		print("<filename> <minimum support> <minimum confidence>")
	else:
		dataset = parse_csv(sys.argv[1])
		assoc_rules = apriori(dataset, float(sys.argv[2]), float(sys.argv[3]))
		for cond, subset, conf in assoc_rules:
			print("({})->({}) conf = {:.2f}".format(', '.join(cond), ', '.join(subset), conf))
