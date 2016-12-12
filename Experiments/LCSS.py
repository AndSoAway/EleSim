#!/usr/bin/python

import sys, os, codecs
from fetch_data import *

class LCSS:

	def __init__(self, ele, indicator, trh, offset):
		self.ele = ele
		self.indicator = indicator
		self.trh = trh
		self.offset = offset
		self.n = len(ele)
		self.m = len(indicator)
		self.res = []
		for i in range(self.n + 1):
			arr = []
			for j in range(self.m + 1):
				arr.append(-1)
			self.res.append(arr)
		for i in range(self.n + 1):
			self.res[i][0] = 0
		for j in range(self.m + 1):
			self.res[0][j] = 0 

	def getSimilarity(self):
		res = self.lcss(self.ele, self.indicator)
		print("res: " + str(res))
		cnt =  float(min(self.n, self.m))
		print("cnt: " + str(cnt))
		return res / cnt

	def isClose(self, ele, indicator):
		n = len(ele)
		m = len(indicator)
		return (abs(ele[-1] - indicator[-1]) < self.trh and abs(n - m) <= self.offset)

	def lcss(self, ele, indicator):
		n = len(ele)
		m = len(indicator)
		if n == 0 or m == 0:
			return 0
		if self.res[n][m] != -1:
			return self.res[n][m]
		if self.isClose(ele, indicator):
			cur = 1.0 + self.lcss(ele[:-1], indicator[:-1])
			self.res[n][m] = cur
		else:
			res1 = self.lcss(ele[:-1], indicator)
			res2 = self.lcss(ele, indicator[:-1])
			cur = max(res1, res2)
			self.res[n][m] = cur
		return self.res[n][m]

if __name__ == '__main__':
	trh = 0.3
	offset = 3
	data = fetch_data()
	res_file = codecs.open('LCSS_Res.csv', 'w', 'GBK')
	for prvn in data:
		array = data[prvn]
		ele = array['ele']
		index = array['val']
		for indicator in index:
			lcss = LCSS(ele, indicator['data'], trh, offset)	
			res = lcss.getSimilarity()
			res_file.write(prvn + ',' + indicator['name'] + ',' + str(res) + os.linesep)
	res_file.close()