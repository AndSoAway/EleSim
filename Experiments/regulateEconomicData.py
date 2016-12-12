#/usr/bin/python
#-*- coding:utf-8 -*-

import os, sys, codecs

#把txt数据整理成csv文件

def process(file_name):
	#print(file_name)
	file = codecs.open(file_name, 'r', 'GB2312')
	isValid = False
	record = []
	headers = []
	for x in file:
		line_parts = x.split(',')
		comm_count = len(line_parts)
		if isValid == False:
			if comm_count > 10:
				isValid = True
		if isValid == True:
			if comm_count < 10:
				isValid = False
		if isValid:
			headers.append(line_parts[0])
			record.append(line_parts[1:])
	output_names = file_name.split('/')
	output_names[len(output_names) - 1] = "Regulate-" + output_names[len(output_names) - 1]
	output_file_name = '/'.join(output_names)
	
	regulate_path_file = codecs.open("regulate_path.txt", 'a', 'utf-8')
	regulate_path_file.write(output_file_name + os.linesep)
	regulate_path_file.close()

	output_file = codecs.open(output_file_name, 'w', 'utf-8')
	head_line = ','.join(headers) + os.linesep
	output_file.write(head_line)
	count = len(record[0])
	for idc in range(count):
		line = record[0][idc]
		for x in record[1:]:
			line = line + ',' + x[idc]
		line = line + os.linesep
		output_file.write(line)
	output_file.close()

if __name__ == "__main__":
	path_txt = 'path.txt'
	path = codecs.open(path_txt, 'r', 'utf-8')
	file_names = []
	for line in path:
		line = line[:line.find(os.linesep)]
		file_names.append(line)

	for file_name in file_names:
		process(file_name)