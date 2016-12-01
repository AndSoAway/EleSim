#/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, codecs

#把天数据转换为月数据

def sumEle(file_name):
	file = codecs.open(file_name, 'r', 'utf-8')
	month_data = []
	sum = 0
	tag = None
	minVal = None
	maxVal = None
	region = None
	for line in file:
		parts = line.split(',')
		ele_num = float(parts[2])
		region = parts[0]
		time = parts[1].split('/')
		year = time[0]
		month = time[1]
		day = time[2]
		cur_tag = year + '/' + month
		if cur_tag != tag:
			if tag is not None:
				month_data.append([tag, sum])
				if minVal is None:
					minVal = sum
					maxVal = sum
				else:
					minVal = min(minVal, sum)
					maxVal = max(maxVal, sum)
			tag = cur_tag
			sum = ele_num
		else:
			sum = sum + ele_num
	print(str(minVal) + ', ' + str(maxVal))
	name_parts = file_name.split('/')
	sum_file_name = name_parts[0] + '/' + name_parts[1] + '/' + "Sum-" + name_parts[2]
	sum_file = codecs.open(sum_file_name, 'w', 'utf-8')
	print(sum_file_name)
	for record in month_data:
		record.append((record[1] - minVal) / (maxVal - minVal))
		sum_file.write(region + ',' + record[0] + ',' + str(record[1]) + ',' + str(record[2]) + os.linesep)
	sum_file.close()

if __name__ == "__main__":
	file_names = ["./Anhui/安徽.csv", "./Shanghai/上海.csv", "./Fujian/福建.csv", "./Zhengjiang/浙江.csv", "./Huadong/华东.csv", "./Jiangsu/江苏.csv"]
	for file in file_names:
		sumEle(file)
