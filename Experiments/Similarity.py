#!/usr/bin/python
#!-*- coding:utf-8 -*-

import codecs, sys, os
import calculateArea

#进行相似性的计算和比较

def process(prvn, fln1, fln2):
	f1 = codecs.open(fln1, 'r', 'utf-8')
	f2 = codecs.open(fln2, 'r', 'utf-8')
	ele = []
	for line in f1:
		line_parts = line.split(',')
		ele.append(float(line_parts[-1]))

	metrics = []
	headers = f2.readline()
	headers = headers[:headers.find(os.linesep)].split(',')
	mtr_cnt = len(headers)
	for x in range(mtr_cnt - 1):
		metrics.append([])

	for line in f2:
		line_parts = line[:line.find(os.linesep)].split(',')
		for idc in range(mtr_cnt - 1):
			mtr = float(line_parts[idc + 1])
			metrics[idc].append(mtr)

	res_file = codecs.open('res_file.txt', 'a', 'utf-8')
	for idc in range(mtr_cnt - 1):
		metric = headers[idc + 1]
		mtr_arr = metrics[idc]
		mtr_arr.reverse()
		sim = similarity(ele, mtr_arr)
		delay = periodity(ele, mtr_arr)
		res_file.write(prvn + "," + metric + "," + str(sim) + "," + str(delay[0]) + "," + str(delay[1]) + os.linesep)
	res_file.close()

def periodity(ele, mtr):
	count = min(len(ele), len(mtr))
	MOVE_MAX = 12
	least_sim = 0
	chose_idc = 0
	for x in range(MOVE_MAX):
		move_mtr_frwr = []
		move_ele_frwr = []

		move_mtr_bckwr = []
		move_ele_bckwr = []
		for num in mtr[x:]:
			move_mtr_frwr.append(num)
		ele_part = ele if x == 0 else ele[:-1 * x]
		for num in ele_part:
			move_ele_frwr.append(num)

		for num in ele[x:]:
			move_ele_bckwr.append(num)
		mtr_part = mtr if x == 0 else mtr[:-1 * x]
		for num in mtr_part:
			move_mtr_bckwr.append(num)
		
		cur_sim1 = similarity(move_ele_frwr, move_mtr_frwr)
		cur_sim2 = similarity(move_ele_bckwr, move_mtr_bckwr)
		print("x: " + str(x) + "cur_sim1: " + str(cur_sim1) + ", cur_sim2: " + str(cur_sim2))
		if cur_sim1 > least_sim:
			least_sim = cur_sim1
			chose_idc = x
		if cur_sim2 > least_sim:
			least_sim = cur_sim2
			chose_idc = -1 * x
	print(str(least_sim) + "," + str(chose_idc))
	return [least_sim, chose_idc]

def similarity(ele, mtr):
	count = min(len(ele), len(mtr))
	least_area = 1000
	#print("Count: " + str(count))
	for x in range(count):
		offset = ele[x] - mtr[x]
		c_arr = []
		for num in mtr:
			c_arr.append(num + offset)
		cur_area = calculateArea.area(ele, c_arr)
		#print("cur_area: " + str(cur_area) + ", least_area: " + str(least_area))
		#print("cur_area is " + str(cur_area) + "least_area: " + str(least_area))
		least_area = min(least_area, cur_area)
	sim = 1 - (least_area / (count - 1))
	#print("Least Sim: " + str(1 - sim))
	return sim

if __name__ == "__main__":
	ele_prvns = ["/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Anhui/sum-安徽.csv",
	"/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Fujian/sum-福建.csv",
	"/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Huadong/sum-华东.csv",
	"/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Jiangsu/sum-江苏.csv",
	"/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Shanghai/sum-上海.csv",
	"/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Zhengjiang/sum-浙江.csv"]
	ele_files = {}
	metric_files = {}
	for flnm in ele_prvns:
		flnm_prts = flnm.split('/')
		prvn = flnm_prts[-2]
		if prvn not in ele_files:
			ele_files[prvn] = flnm
			metric_files[prvn] = []

	select_txt = "select_path.txt"
	select_flnms = codecs.open(select_txt, 'r', 'utf-8')
	for flnm in select_flnms:
		flnm = flnm[:flnm.find(os.linesep)]
		flnm_parts = flnm.split('/')
		prvn = flnm_parts[-1].split('-')[0]
		if prvn in metric_files:
			metric_files[prvn].append(flnm)
		else:
			print("Exception: Metrics has no responding Provinces")

	for prvn in ele_files:
		for mtr_fl in metric_files[prvn]:
			process(prvn, ele_files[prvn], mtr_fl) 