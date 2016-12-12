#!/usr/bin/python
#-*- coding:utf-8 -*-

import codecs, sys, os

def splitIndicatorProvinces(flnms):
	prefix = "../Data/"
	prvns = {}
	all_index = []
	all_index.append('日期')
	time = []
	for flnm in flnms:
		flnm_parts = flnm.split('/')
		index_name = flnm_parts[-1].split('.')[0]
		print(isinstance(index_name, str))
		all_index.append(index_name)
		
		file = codecs.open(flnm, 'r', 'utf-8')
		headers = file.readline()
		headers = headers[:headers.find(os.linesep)]
		if len(time) < 1:
			time = headers.split(',')[1:]

		record = {}
		for line in file:
			line = line[:line.find(os.linesep)]
			line_parts = line.split(',')
			prvn = line_parts[0]
			if prvn not in prvns:
				prvns[prvn] = {}
			if index_name not in prvns[prvn]:
				prvns[prvn][index_name] = line.split(',')[1:]

	time_count = len(time)
	for prvn in prvns:
		otpt_fl = prefix + prvn[:-1].encode('utf-8') + "价格指数.csv"
		otpt = codecs.open(otpt_fl, 'w', 'utf-8')
		head_line = ','.join(all_index) + os.linesep
		otpt.write(head_line.decode('utf-8'))
		for x in range(time_count):
			cur_line = time[x]
			for index in all_index[1:]:
				cur_line = cur_line + ',' + prvns[prvn][index][x]
			cur_line = cur_line + os.linesep
			otpt.write(cur_line)
		otpt.close()

def splitElecProvinces(flnm):
	file = codecs.open(flnm, 'r', 'GB2312')
	headers = file.readline()
	headers = headers[:headers.find(os.linesep)]
	record = {}
	for line in file:
		line = line[:line.find(os.linesep)]
		line_parts = line.split(',')
		prvn = line_parts[0]
		if prvn not in record:
			record[prvn] = []
		record[prvn].append(line)
	for prvn in record:
		records = record[prvn]
		flnm_parts = flnm.split('/')
		flnm_parts[-1] = prvn.encode('utf-8') + "-" + flnm_parts[-1]
		otpt_fl = '/'.join(flnm_parts)
		print(otpt_fl)
		otpt = codecs.open(otpt_fl, 'w', 'utf-8')
		otpt.write(headers + os.linesep)
		for rcrd in records:
			otpt.write(rcrd + os.linesep)
		otpt.close()
	file.close()

if __name__ == "__main__":
	flnm = "../Data/调度数据中心.csv"
	flnms = ["../Data/居民消费价格指数.csv", "../Data/居住类居民消费价格指数.csv", 
"../Data/衣着类居民消费价格指数.csv",
"../Data/医疗保健类居民消费价格指数.csv",
"../Data/食品烟酒类居民消费价格指数.csv",
"../Data/交通和通信类居民消费价格指数.csv",
"../Data/其他用品和服务类居民消费价格指数.csv",
"../Data/教育文化和娱乐类居民消费价格指数.csv",
"../Data/生活用品及服务类居民消费价格指数.csv"]
	splitIndicatorProvinces(flnms)
