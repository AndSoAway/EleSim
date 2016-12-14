#!/usr/bin/python
#!-*- coding:utf-8 -*-

import codecs, sys, os
import calculateArea
from fetch_data import *

#进行相似性的计算和比较
class AreaSim:

	def __init__(self, ele, indicator):
		self.n = len(ele)
		self.m = len(indicator)
		self.min_len = min(self.n, self.m)
		self.ele = ele[:self.min_len]
		self.indicator = indicator[:self.min_len]

	def areaSim(self, ele, indicator):
		least_area = 1000
		length = len(ele)
		for x in range(length):
			offset = ele[x] - indicator[x]
			c_arr = []
			for num in indicator:
				c_arr.append(num + offset)
			cur_area = calculateArea.area(ele, c_arr)
			least_area = min(least_area, cur_area)
		sim = 1 - (least_area / (self.min_len - 1))
		return sim

	def getSimilarity(self):
		sim = self.areaSim(self.ele, self.indicator)
		return sim

	def getLagging(self):
		ele = self.ele[12:-12]
		indicator = self.indicator
		MOVE_MAX = 12
		sim_max = 0
		offset = 0
		for x in range(12):
			cur_indc = indicator[11-x:-13-x]
			cur_sim = self.areaSim(ele, cur_indc)
			if cur_sim > sim_max:
				sim_max = cur_sim
				offset = x + 1
			cur_indc = indicator[13+x:] if x == 11 else indicator[13+x:-11+x]
			cur_sim = self.areaSim(ele, cur_indc)
			if cur_sim > sim_max:
				sim_max = cur_sim
				offset = -(x + 1)
		return [sim_max, offset]

if __name__ == "__main__":
	data = fetch_data()

	res_file = codecs.open('Area_Sim.csv', 'w', 'GBK')
	for prvn in data:
		prvn_data = data[prvn]
		ele = prvn_data['ele']
		index = prvn_data['val']
		for indicator in index:
			areaSim = AreaSim(ele, indicator['data'])
			ori = areaSim.getSimilarity()
			lagging = areaSim.getLagging()
			if ori > lagging[0]:
				lagging[0] = ori
				lagging[1] = 0
			res_file.write(prvn + ',' + indicator['name'] + ',' + str(ori) + ',' + str(lagging[0]) + ',' + str(lagging[1]) + os.linesep)
	res_file.close()