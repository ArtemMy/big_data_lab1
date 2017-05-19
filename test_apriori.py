#!/usr/bin/python3
import unittest
import apriori
import collections
from collections import defaultdict

class TestApriori(unittest.TestCase):

    def make_itemset(self, list):
        return set(map(frozenset, list))

    def test_get_items(self):
        in1 = [["a", "b","c"], ["b", "c", "d"], ["c", "d"]]
#        out1 = set(map(frozenset, ["a", "b", "c", "d"]))
        out1 = self.make_itemset(["a", "b", "c", "d"])
        self.assertEqual(apriori.get_items(in1), out1)
 
        in2 = [["a", "b"], ["c", "d", "e"]]
        out2 = self.make_itemset(["a", "b", "c", "d", "e"])
        self.assertEqual(apriori.get_items(in2), out2)
 
        self.assertEqual(apriori.get_items([]), self.make_itemset([]))

    def test_min_support_items(self):
        dataset = [["a", "b","c"], ["b", "c", "d"], ["c", "d"]]
        freq_dict = defaultdict(int)
        itemset1 = self.make_itemset(["a", "b", "c", "d"])
        freq_out = dict(zip(map(frozenset, ["a", "b", "c", "d"]), [1, 2, 3, 2]))

        min_sup1 = apriori.min_support_items(itemset1, dataset, 0, freq_dict)
        self.assertEqual(min_sup1, itemset1)
        for item in min_sup1:   
            self.assertTrue(item in freq_dict)

        self.assertEqual(freq_out, dict(freq_dict))

        freq_dict = defaultdict(int)
        itemset2 = self.make_itemset([["a", "b"], ["c", "d"]])
        out2 = self.make_itemset([["c", "d"]])
        self.assertEqual(apriori.min_support_items(itemset2, dataset, 1/2, freq_dict), out2)
        self.assertEqual(apriori.min_support_items(itemset2, dataset, 0, freq_dict), itemset2)
        self.assertEqual(apriori.min_support_items(itemset2, dataset, 1, freq_dict), set())
        freq_dict = defaultdict(int)
        itemset3 = self.make_itemset([["a", "d"]])
        out3 = self.make_itemset([["c", "d"]])
        self.assertEqual( apriori.min_support_items(itemset3, dataset, 0, freq_dict), set())

    def test_gen_candidates(self):
        in1 = set(self.make_itemset([["a", "b", "c"], ["b", "c", "d"], ["c", "d", "e"]]))
        out1 = set(self.make_itemset([["a", "b", "c", "d"], ["b", "c", "d", "e"]]))
        self.assertEqual(apriori.gen_candidates(in1, 4), out1)

        in2 = set(self.make_itemset([["a", "b"], ["c", "d"]]))
        out2 = set()
        self.assertEqual(apriori.gen_candidates(in2, 3), out2)
        self.assertEqual(apriori.gen_candidates(set(), 1), set())

    def test_k_item_set(self):
        return
if __name__ == '__main__':
    unittest.main()