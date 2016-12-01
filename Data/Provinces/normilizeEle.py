#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os, sys, codecs

def normilize(file_name):
    file = codecs.open(file_name, "r", "utf-8")
    records = []
    for x in file:
        records.append(x)
    file.close()
    first = records[0]
    parts = first.split(',')
    minVal = float(parts[2])
    maxVal = float(parts[2])
    for line in records:
    	parts = line.split(',')
    	elec_num = float(parts[2])
    	minVal = min(minVal, elec_num)
    	maxVal = max(maxVal, elec_num)
    cur_records = []
    for line in records:
    	parts = line.split(',')
    	elec_num = float(parts[2])
    	nor_num = (elec_num - minVal) / (maxVal - minVal)
    	cur_line = parts[0] + ',' + parts[1] + ',' + str(nor_num) + os.linesep
        cur_records.append(cur_line)
    file_parts = file_name.split('/')
    norm_file_name = "./" + file_parts[1] + '/' + "Norm_" + file_parts[2]
    nor_file = codecs.open(norm_file_name, 'w', 'utf-8')
    for line in cur_records:
    	nor_file.write(line)
    nor_file.close()

if __name__ == "__main__":
    file_names = ["./Anhui/安徽.csv", "./Fujian/福建.csv", "./Huadong/华东.csv", "./Jiangsu/江苏.csv", "./Shanghai/上海.csv", "./Zhengjiang/浙江.csv"]
    for file_name in file_names:
    	normilize(file_name)
   


