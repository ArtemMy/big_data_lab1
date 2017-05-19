import unittest
import test_fp_growth, test_apriori, test_common
import common, apriori, fp_growth

def test_equal_and_right(data, min_conf, min_supp):
	dataset = common.parse_csv(data)
	apr_res = set(apriori.apriori(dataset, min_supp, min_conf))
	fp_gr_res = set(fp_growth.fp_growth(dataset, min_supp, min_conf))
	if not apr_res == fp_gr_res:
		return False
	items_freq = {}
	for cond, itemset, conf in apr_res:
		items_freq[cond] = 0
		items_freq[cond.union(itemset)] = 0
	for row in dataset:
		for item in items_freq:
			if item.issubset(row):
				items_freq[item] += 1
	for cond, itemset, conf in apr_res:
		if items_freq[cond.union(itemset)] < min_supp * len(dataset):
			return False
		if items_freq[cond.union(itemset)] / items_freq[cond] < min_conf:
			return False
	return True
	
if __name__ == '__main__':
	suite_common = unittest.TestLoader().loadTestsFromTestCase(test_common.TestCommon)
	suite_apr = unittest.TestLoader().loadTestsFromTestCase(test_apriori.TestApriori)
	suit_fr_p = unittest.TestLoader().loadTestsFromTestCase(test_fp_growth.TestFPGrowth)
	alltests = unittest.TestSuite([suite_common, suite_apr, suit_fr_p])
	unittest.TextTestRunner(verbosity=2).run(alltests)

	print("comparing apriori and fp_growth and checking results... ")
	ok = test_equal_and_right("dataset/1000.csv", 0.4, 0.005)
	ok = ok and test_equal_and_right("dataset/1000.csv", 0.3, 0.05)
	ok = ok and test_equal_and_right("dataset/1000.csv", 0.5, 0.01)
	if ok:
		print("OK")
	else:
		print("FAILED")