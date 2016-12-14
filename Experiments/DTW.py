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
		
	def initRes(self):
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
		min_len = min(n, m)
		self.initRes()
		res = 1 - self.dtw(self.ele[:min_len], self.indicator[:min_len]) / min_len
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
			cur_indc = indicator[11-x:-13-x]
			#print(str(cur_indc))
			self.initRes()
			cur_sim = 1 - self.dtw(ele, cur_indc) / all_len
			#print("cur_sim: " + str(cur_sim) + ", offset: " + str(x))
			if cur_sim > sim_max:
				sim_max = cur_sim
				offset = x + 1
			cur_indc = indicator[13+x:] if x == 11 else indicator[13+x:-11+x]
			cur_sim = 1 - self.dtw(ele, cur_indc) / all_len
			if cur_sim > sim_max:
				sim_max = cur_sim
				offset = -(x + 1)
		return [sim_max, offset]

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
	data = fetch_data()
	
	res_file = codecs.open('DTW_Res.csv', 'w', 'GBK')
	for prvn in data:
		array = data[prvn]
		ele = array['ele']
		index = array['val']
		for indicator in index:
			dtw = DTW(ele, indicator['data'])
			ori = dtw.getSimilarity()
			lagging = dtw.getLagging()
			if ori > lagging[0]:
				lagging[0] = ori
				lagging[1] = 0
			res_file.write(prvn + ',' + indicator['name'] + ',' + str(ori) + ',' + str(lagging[0]) + ',' + str(lagging[1]) + os.linesep)
	res_file.close()