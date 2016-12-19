#!/usr/bin/python
#-*- coding:utf-8 -*-

import os, sys, codecs

def parallel(flnm):
	file = codecs.open(flnm, 'r', 'utf-8')
	data = {}
	headers = []


	ele_file = codecs.open('../Data/Provinces/Anhui/sum-安徽.csv', 'r', 'utf-8')
	ele_arr = []
	for line in ele_file:
		line = line[:line.find(os.linesep)]
		line_parts = line.split(',')
		ele_arr.append(line_parts[-1])
	ele_arr.reverse()
	data['ele'] = ele_arr
	headers.append('ele')

	pre_arr = []
	count = 0
	for line in file:
		line = line[:line.find(os.linesep)]	
		if len(line) < 1:
			continue
		if line[0] == '#':
			headers.append(line)
			data[line] = pre_arr[1:]
			count = len(pre_arr) - 1
			pre_arr = []
		else:
			pre_arr.append(line)
	file.close()

	res = codecs.open('ParalTop-1.csv', 'w', 'GBK')
	res.write(' '.join(headers) + os.linesep)
	for x in range(count):
		cur_line = []
		for header in headers:
			cur_line.append(data[header][x])
		res.write(' '.join(cur_line) + os.linesep)
	res.close()

if __name__ == "__main__":
	file_name = "Top-1.csv"
	parallel(file_name)