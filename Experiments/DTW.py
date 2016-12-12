#!/usr/bin/python

import os, sys, codecs
from fetch_data import *

class DTW:

	def __init__(self, ele, indicator):
		self.ele = ele
		self.indicator = indicator
		self.n = len(ele)
		self.m = len(indicator)
		self.res = []
		for i in range(self.n + 1):
			arr = []
			for j in range(self.m + 1):
				arr.append(-1)
			self.res.append(arr)
		for i in range(self.n + 1):
			self.res[i][0] = float('inf')
		for j in range(self.m + 1):
			self.res[0][j] = float('inf')
		self.res[0][0] = 0

	def distance(self, p1, p2):
		return float(abs(p1 - p2))

	def getSimilarity(self):
		n = len(self.ele)
		m = len(self.indicator)
		res = 1 - self.dtw(self.ele, self.indicator) / max(n, m)
		return res

	def dtw(self, ele, indicator):
		n = len(ele)
		m = len(indicator)
		#print("n: " + str(n) + ", m: " + str(m))
		if self.res[n][m] != -1:
			return self.res[n][m]
		if n == 0 and m == 0:
			return 0
		if n == 0:
			return self.res[0][m]
		if m == 0:
			return self.res[0][n]
		res1 = self.dtw(ele[1:], indicator)
		res2 = self.dtw(ele, indicator[1:])
		res3 = self.dtw(ele[1:], indicator[1:])
		#print("res1: " + str(res1) + ", res2: " + str(res2) + ", res3: " + str(res3))
		self.res[n][m] = self.distance(ele[0], indicator[0]) + min(res1, min(res2, res3))
		#print("n " + str(n) + ", " + str(m) + "," + str(self.res[n][m]))
		return self.res[n][m]

if __name__ == '__main__':
	#ele = [1, 1]
	#arr = [1, 2]
	#dtw = DTW(ele, arr)
	#res = dtw.getSimilarity()
	#print("res:" + str(res))

	data = fetch_data()
	res_file = codecs.open('DTW_Res.csv', 'w', 'GBK')
	for prvn in data:
		array = data[prvn]
		ele = array['ele']
		index = array['val']
		for indicator in index:
			dtw = DTW(ele, indicator['data'])
			res = dtw.getSimilarity()
			res_file.write(prvn + ',' + indicator['name'] + ',' + str(res) + os.linesep)
	res_file.close()