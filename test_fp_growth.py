#!/usr/bin/python3
import unittest
import fp_growth
import collections
from collections import defaultdict

class TestFPGrowth(unittest.TestCase):
    def make_itemset(self, list):
        return set(map(frozenset, list))
    def make_notiter_itemset(self, list):
        set(x for x in make_itemset(self, list))
    def default_tree(self):
        tree = fp_growth.FPTree()
        tree.insert(["a", "b", "c"])
        tree.insert(["b", "a", "d"], 2)
        tree.insert(["b", "d"])
        return tree

    def test_add_child(self):
        node = fp_growth.Node("node")
        child =fp_growth.Node("child")
        node.add_child(child)
        self.assertTrue(child.item in node.children)

    def test_new_node(self):
        tree = fp_growth.FPTree()
        n1 = tree.new_node("a", tree.root)
        self.assertEqual(n1.parent, tree.root)
        self.assertEqual(n1.count, 0)
        n2 = tree.new_node("b", tree.root)
        self.assertEqual(n2.parent, tree.root)
        n3 = tree.new_node("a", n2)
        self.assertEqual(n3.parent, n2)
        self.assertEqual(tree.root.children, {"a" : n1, "b" : n2})
        self.assertEqual(tree.itemset["a"], n3)
        self.assertEqual(tree.itemset["a"].neighbour, n1)

    def test_insert(self):
        tree = fp_growth.FPTree()
        t1 = ["a", "b", "c"]
        tree.insert(t1)
        self.assertTrue(t1[0] in tree.root.children)
        self.assertTrue(t1[1] in tree.root.children[t1[0]].children)
        self.assertTrue(t1[2] in tree.root.children[t1[0]].children[t1[1]].children)
        self.assertEqual(tree.root.children[t1[0]].count, 1)
        t2 = ["a", "b", "d"]
        tree.insert(t2, 2)
        self.assertEqual(tree.root.children[t1[0]].count, 3)
        self.assertEqual(tree.root.children[t2[0]].children[t2[1]].count, 3)
        self.assertEqual(tree.root.children[t2[0]].children[t2[1]].children[t2[2]].count, 2)
    def test_support(self):
        tree = self.default_tree()
        self.assertEqual(tree.support("a"), 3)
        self.assertEqual(tree.support("b"), 4)
        self.assertEqual(tree.support("c"), 1)
        self.assertEqual(tree.support("d"), 3)
    def test_prefix_path(self):
        tree = self.default_tree()
        path = list(tree.get_prefix_path(tree.root.children["b"].children["a"].children["d"]))
        self.assertEqual(path, [tree.root.children["b"].children["a"], tree.root.children["b"]])
    def test_conditional_pattern_base(self):
        tree = self.default_tree()
        path, count = zip(*list(tree.get_conditional_pattern_base("a")))
        self.assertEqual(list(zip(map(list, path), count)), [(["b"], 2), ([], 1)])
        path, count = zip(*list(tree.get_conditional_pattern_base("d")))
        self.assertEqual(list(zip(map(list, path), count)), [(["b"], 1), (["b", "a"], 2)])
    def test_get_items_freq(self):
        dataset = [["a", "b", "c"], ["b", "a", "d"], ["b", "d"]]
        freq = fp_growth.get_items_freq(dataset)
        self.assertEqual(freq, {"a": 2, "b" : 3, "c" : 1, "d" : 2})
    def test_create_tree(self):
        dataset = [["a", "b", "c"], ["b", "a", "d"], ["b", "d"]]
        freq = {"a": 2, "b" : 3, "c" : 1, "d" : 2}
        tree = fp_growth.create_tree(dataset, freq)
        dataset = map(lambda row: sorted(row, key=lambda item: freq[item], reverse=True), dataset)
        for itemset in dataset:
            node = tree.root
            for item in itemset:
                self.assertTrue(item in node.children)
                node = node.children[item]
    def test_create_conditional_tree(self):
        paths = [(["b", "a"], 2), (["b", "c"], 1)]
        tree = fp_growth.crete_conditional_tree(paths)
        self.assertEqual(tree.root.children["b"].count, 3)
        self.assertEqual(tree.root.children["b"].children["a"].count, 2)
        self.assertEqual(tree.root.children["b"].children["c"].count, 1)

if __name__ == '__main__':
    unittest.main()
