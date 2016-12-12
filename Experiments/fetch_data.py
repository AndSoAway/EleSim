#!/usr/bin/python
#-*- coding:utf-8 -*-

import codecs, sys, os

def get_ele(ele):
	f1 = codecs.open(ele, 'r', 'utf-8')
	ele = []
	for line in f1:
		line_parts = line.split(',')
		ele.append(float(line_parts[-1]))
	return ele

def get_data(mtr_fl):
	f2 = codecs.open(mtr_fl, 'r', 'utf-8')
	metrics = []
	headers = f2.readline()
	headers = headers[:headers.find(os.linesep)].split(',')
	mtr_cnt = len(headers)
	for x in range(mtr_cnt - 1):
		metrics.append({"name": headers[x + 1], "data":[]})

	for line in f2:
		line_parts = line[:line.find(os.linesep)].split(',')
		for idc in range(mtr_cnt - 1):
			mtr = float(line_parts[idc + 1])
			metrics[idc]['data'].append(mtr)
	return metrics

#Get: Province: ['ele': ] ['val': []]

def fetch_data():
	ele_prvns = ["/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Anhui/sum-安徽.csv",
	"/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Fujian/sum-福建.csv",
	"/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Huadong/sum-华东.csv",
	"/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Jiangsu/sum-江苏.csv",
	"/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Shanghai/sum-上海.csv",
	"/Users/xieyongqing/Desktop/ElecSim/Data/Provinces/Zhejiang/sum-浙江.csv"]
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

# ele_files 表示 各省的用电量
# metric_files 表示 各省所对应的指标情况
#
	data = {}
	for prvn in ele_files:
		for mtr_fl in metric_files[prvn]:
			if prvn not in data:
				data[prvn] = {}
				data[prvn]['ele'] = get_ele(ele_files[prvn])
				data[prvn]['val'] = []
			data_array = get_data(mtr_fl)
			for array in data_array:
				data[prvn]['val'].append(array)
	return data

if __name__ == "__main__":
	array = fetch_data()
	for prvn in array:
		print(prvn)
		print(type(array[prvn]))
