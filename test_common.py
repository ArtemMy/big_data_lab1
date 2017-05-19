#!/usr/bin/python3
import common
import unittest

class TestCommon(unittest.TestCase):

    def make_itemset(self, list):
        return set(map(frozenset, list))

    def test_all_combinations(self):
        out1 = self.make_itemset([["a"], ["b"]])
        self.assertEqual(set(common.all_combinations(frozenset(["a", "b"]))), out1)
        self.assertEqual(set(common.all_combinations(frozenset("a"))), set())
        out2 = self.make_itemset([["a"], ["b"], ["c"], ["a", "b"], ["a", "c"], ["c", "b"]])
        self.assertEqual(set(common.all_combinations(frozenset(["a", "b", "c"]))), out2)

    def test_gen_rules(self):
        support = { frozenset(["a"]) : 10, frozenset(["b"]): 20, frozenset(["a", "b"]) : 5 }
        itemset = frozenset(["a", "b"])
        out1 = set([(frozenset("a"), frozenset("b"), 0.5)])
        out2 = set([(frozenset("b"), frozenset("a"), 0.25), (frozenset("a"), frozenset("b"), 0.5)])
        out3 = set()
        self.assertEqual(set(common.gen_rules(itemset, support, 0.5)), out1)
        self.assertEqual(set(common.gen_rules(itemset, support, 0.1)), out2)
        self.assertEqual(set(common.gen_rules(itemset, support, 0.7)), out3)

if __name__ == '__main__':
    unittest.main()