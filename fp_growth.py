 #!/usr/bin/python3

from common import gen_rules, parse_csv
import sys
from collections import defaultdict

def print_tree(node):
	print("{}: {} x {}".format(node.item, node.children.keys(), node.count))
	for item in node.children:
		print_tree(node.children[item])

class Node(object):
	def __init__(self, item, parent=None):
		self.item = item
		self.parent = parent
		self.count = 0
		self.neighbour = None
		self.children = {}

	def add_child(self, child):
		self.children[child.item] = child

class FPTree(object):
	def __init__(self):
		self.root = Node(None)
		self.itemset = {}

	def new_node(self, item, parent):
		node = Node(item, parent)
		if item in self.itemset:
			node.neighbour = self.itemset[item]
		self.itemset[item] = node
		parent.add_child(node)
		return node

	def insert(self, transaction, count = 1):
		top = self.root
		for item in transaction:
			top = top.children[item] if item in top.children else self.new_node(item, top)
			top.count += count 
		# while transaction:
		# 	res = next((top.children[item] for item in transaction if item in top.children), None)
		# 	top = res if res else self.new_node(transaction[0], top)
		# 	top.count += count 
		# 	transaction.remove(top.item)

	def support(self, item):
		supp = 0
		node = self.itemset[item]
		while node:
			supp += node.count
			node = node.neighbour
		return supp

	def get_prefix_path(self, node):
		if(node):
			node = node.parent
		while node and node.count != 0:
			yield node
			node = node.parent

	def get_conditional_pattern_base(self, item):
		if not item in self.itemset:
			return
		node = self.itemset[item]
		while node: # and node.count != 0:
			prefix_p = reversed([x.item for x in self.get_prefix_path(node)])
			yield prefix_p, node.count
			node = node.neighbour

def get_items_freq(dataset):
	items_freq = defaultdict(int)
	for row in dataset:
		for item in row:
			if item:
				items_freq[item] += 1
	return items_freq

def create_tree(dataset, itemset_freq):
	fp_tree = FPTree()
	for row in dataset:
		row.sort(key=lambda item: itemset_freq[item], reverse=True)
		fp_tree.insert(row)
	return fp_tree

def crete_conditional_tree(paths):
	fp_tree = FPTree()
	for path, count in paths:
		fp_tree.insert(path, count)
	return fp_tree

def fp_growth(dataset, min_support, min_conf):
	itemset_freq = get_items_freq(dataset)
	fp_tree = create_tree(dataset, itemset_freq)
	min_support_abs = min_support * len(dataset)
	fp_support = {}

	def fp_from_tree(tree, suffix):
		for item in sorted(tree.itemset, key=lambda item: itemset_freq[item], reverse=False):
			item_support = tree.support(item)
			if item_support >= min_support_abs and item not in suffix:
				fp = [item] + suffix
				assert(len(frozenset(fp)) == len(suffix) + 1)
				fp_support[frozenset(fp)] = item_support

				condtree = crete_conditional_tree(tree.get_conditional_pattern_base(item))
				fp_from_tree(condtree, fp)
	fp_from_tree(fp_tree, [])
	for itemset in fp_support.keys():
		yield from gen_rules(itemset, fp_support, min_conf)

if __name__ == "__main__":
	if(len(sys.argv) < 4):
		print("<filename> <minimum support> <minimum confidence>")
	else:
		dataset = parse_csv(sys.argv[1])
		assoc_rules = fp_growth(dataset, float(sys.argv[2]), float(sys.argv[3]))
		for cond, subset, conf in assoc_rules:
			print("({})->({}) conf = {:.2f}".format(', '.join(cond), ', '.join(subset), conf))