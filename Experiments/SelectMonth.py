#/usr/bin/python
#-*- coding:utf-8 -*-

import os, sys, codecs

def select(file_name):
	file = codecs.open(file_name, 'r', 'utf-8')
	headers = file.readline().split(',')
	field_count = len(headers)
	for x in range(field_count):
		print("x " + str(x) + ", headers[x]: " + headers[x])
	print(field_count)
	records = []
	for line in file:
		line = line[:line.find(os.linesep)]
		line_parts = line.split(',')
		time = line_parts[0]
		#print(line)
		year = int(time[:4])
		month = time[5:6]
		if year >= 2011:
			records.append(line_parts)
		else:
			break
	record_count = len(records)
	#print("record_count " + str(record_count))
	r_idc = 0
	for record in records:
		for idc in range(field_count):
			if r_idc == 0:
				print("idc: " + str(idc) + "record[idc]: " + record[idc] + "\end")
			if record[idc] == '' or record[idc] == os.linesep:
				if r_idc - 12 < 0:
					#print("Less r_idc: " + str(r_idc))
					valid_number = 0
					incre_number = 1
					sum = 0
					while valid_number < 2:
						cur_r_idc = r_idc + incre_number * 1
						#print(str(cur_r_idc) + ", idc:" + str(idc))
						if records[cur_r_idc][idc] != '':
							sum = sum + float(records[cur_r_idc][idc])
							valid_number = valid_number + 1
						incre_number = incre_number + 1
					record[idc] = str(sum / valid_number)
					if idc == 52 and r_idc == 0:
						print(','.join(record))
				elif r_idc + 12 >= record_count:
					valid_number = 0
					decre_number = 1
					sum = 0
					while valid_number < 2:
						cur_r_idc = r_idc - decre_number * 1
						if records[cur_r_idc][idc] != '':
							sum = sum + float(records[cur_r_idc][idc])
							valid_number = valid_number + 1
						decre_number = decre_number + 1
					record[idc] = str(sum / valid_number)
				else:
					sum = float(records[r_idc - 12][idc])
					valid_number = 0
					incre_number = 1
					#print("r_idc is: " + str(r_idc))
					while valid_number < 1:
						cur_r_idc = r_idc - incre_number * 1
						#print("Cur_r_idc " + str(cur_r_idc) + ", idc " + str(idc))
						if records[cur_r_idc][idc] != '':
							sum = sum + float(records[cur_r_idc][idc])
							valid_number = valid_number + 1
						incre_number = incre_number + 1
					record[idc] = str(sum / 2)
		r_idc = r_idc + 1
	file_name_parts = file_name.split('/')


	file_name_parts[-1] = "Select" + file_name_parts[-1][8:]
	output_file_name = '/'.join(file_name_parts[:6]) + "/Select/" + file_name_parts[-2] + "-"+ file_name_parts[-1]
	output_file = codecs.open(output_file_name, 'w', 'utf-8')
	
	select_path = codecs.open('select_path.txt', 'a', 'utf-8')
	select_path.write(output_file_name + os.linesep)
	select_path.close()

	output_file.write(','.join(headers))
	minVal = []
	maxVal = []
	field_idc = 0
	print(','.join(records[0]))
	for x in records[0][1:]:
		field_idc = field_idc + 1
		#print("field_idc: " + str(field_idc) + "x :" + str(x))
		val = float(x)
		minVal.append(val)
		maxVal.append(val)
	for record in records[1:]:
		for idc in range(field_count - 1):
			val = float(record[idc + 1])
			minVal[idc] = min(minVal[idc], val)
			maxVal[idc] = max(maxVal[idc], val)
	for record in records[1:]:
		for idc in range(field_count - 1):
			val = float(record[idc + 1])
			cur_val = (val - minVal[idc]) / (maxVal[idc] - minVal[idc])
			record[idc + 1] = str(cur_val)
		output_file.write(','.join(record) + os.linesep)
	output_file.close()

if __name__ == "__main__":
	rglt_pt_txt = "regulate_path.txt"
	file_names = codecs.open(rglt_pt_txt, 'r', 'utf-8')
	for file_name in file_names:
		file_name = file_name[:file_name.find(os.linesep)]
		select(file_name)