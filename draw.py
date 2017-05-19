from apriori import apriori as apr
from fp_growth import fp_growth as fp_gr
import common
import matplotlib.pyplot as plt
import collections
import time
import sys 
from functools import partial

def alg_time(dataset, min_supp, min_conf, func):
	start_time = time.time()
	a = [x for x in func(dataset, min_supp, min_conf)]
	print(len(a))
	return time.time() - start_time

def volume(dataset, min_supp, min_conf, n):
	plt.figure(1)
	max_l = len(dataset)
	rng = range(int(max_l / n), max_l + 1, int(max_l / n))
	fp_g_t = [alg_time(dataset[:i], min_supp, min_conf, fp_gr) for i in rng]
	apr_t = [alg_time(dataset[:i], min_supp, min_conf, apr) for i in rng]

	plt.plot(rng, apr_t, color='red', label="apriori")
	plt.hold(True)
	plt.plot(rng, fp_g_t, color='blue', label="fp_growth")

	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

	plt.ylabel('time')
	plt.xlabel('dataset size')
	plt.show()

def supp(dataset, min_supp, min_conf, n):
	plt.figure(2)
	rng = range(1, n + 1)
	step = min_supp / n
	fp_g_t = [alg_time(dataset, step * i, min_conf, fp_gr) for i in rng]
	apr_t = [alg_time(dataset, step * i, min_conf, apr) for i in rng]

	plt.plot(rng, apr_t, color='red', label="apriori")
	plt.hold(True)
	plt.plot(rng, fp_g_t, color='blue', label="fp_growth")
	plt.ylabel('time')
	plt.xlabel('min support')
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	plt.show()

if __name__ == '__main__':
	dataset = common.parse_csv("dataset/1000.csv")
	if (len(sys.argv) > 1 and sys.argv[1] == "volume"):
		rng, apr_t, fp_g_t = volume(dataset, 0.02, 0.4, 5)
	else:
		rng, apr_t, fp_g_t = supp(dataset, 0.01, 0.4, 5)