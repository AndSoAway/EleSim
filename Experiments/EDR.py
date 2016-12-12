#!/usr/bin/python

import os, sys, codecs
from fetch_data import *
class Edr:
	
	def __init__(self, ele, indicator, trh):
		self.ele = ele
		self.indicator = indicator
		self.trh = trh
		self.n = len(ele)
		self.m = len(indicator)
		self.res = []
		for i in range(self.n + 1):
			arr = []
			for j in range(self.m + 1):
				arr.append(-1)
			self.res.append(arr)
		for i in range(self.n + 1):
			self.res[i][0] = i
		for j in range(self.m + 1):
			self.res[0][j] = j

	def subcost(self, v1, v2):
		offset = abs(v1 - v2)
		return 0 if offset < self.trh else 1.0

	def getSimilarity(self):
		res = 1 - self.edr(self.ele, self.indicator) / max(self.n, self.m)
		return res

	def edr(self, ele, indicator):
		n = len(ele)
		m = len(indicator)
		if self.res[n][m] != -1:
			return self.res[n][m]
		if n == 0:
			return m
		if m == 0:
			return n
		res1 = self.edr(ele[1:], indicator[1:]) + self.subcost(ele[0], indicator[0])
		res2 = self.edr(ele[1:], indicator) + 1.0
		res3 = self.edr(ele, indicator[1:]) + 1.0
		#print("Res1: " + str(res1) + ', Res2: ' + str(res2) + ', Res3: ' + str(res3))
		self.res[n][m] = min(min(res1, res2), res3)
		return self.res[n][m]

if __name__ == "__main__":
	# a1 = [0.5, 0.4, 0.3]
	# a2 = [0.2, 0.6, 0.4]
	# edr = Edr(a1, a2, 0.2)
	# print(edr.getSimilarity())
	trh = 0.3
	data = fetch_data()
	res_file = codecs.open('EDR_Res.csv', 'w', 'GBK')
	for prvn in data:
		array = data[prvn]
		ele = array['ele']
		index = array['val']
		for indicator in index:
			#print(str(len(ele)) + ", " + str(len(indicator)))
			edr = Edr(ele, indicator['data'], trh)
			res = edr.getSimilarity()
			print("res:" + str(res))
			res_file.write(prvn + ',' + indicator['name'] + ',' + str(res) + os.linesep)
	res_file.close()