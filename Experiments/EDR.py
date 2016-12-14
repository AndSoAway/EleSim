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

	def initRes(self):
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
		n = len(self.ele)
		m = len(self.indicator)
		min_len = min(n, m)
		self.initRes()
		res = 1 - self.edr(self.ele[:min_len], self.indicator[:min_len]) / min_len
		return res

	def getLagging(self):
		n = len(self.ele)
		m = len(self.indicator)
		min_len = min(n, m)
		ele = self.ele[:min_len][12:-12]
		indicator = self.indicator[:min_len]
		all_len = len(ele)
		sim_max = float('-inf')
		offset = 0
		for x in range(12):
			cur_indc = indicator[11-x:13-x]
			self.initRes()
			cur_sim = 1 - self.edr(ele, cur_indc) / all_len
			if cur_sim > sim_max:
				sim_max = cur_sim
				offset = x + 1
			cur_indc = indicator[13+x:] if x == 11 else indicator[13+x:-11+x]
			cur_sim = 1 - self.edr(ele, cur_indc) / all_len
			if cur_sim > sim_max:
				sim_max = cur_sim
				offset = -(x + 1)
		return [sim_max, offset]

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
			ori = edr.getSimilarity()
			lagging = edr.getLagging()
			if ori > lagging[0]:
				lagging[0] = ori
				lagging[1] = 0
			#print("res:" + str(res))
			res_file.write(prvn + ',' + indicator['name'] + ',' + str(ori) + ',' + str(lagging[0]) + ',' + str(lagging[1]) + os.linesep)
	res_file.close()