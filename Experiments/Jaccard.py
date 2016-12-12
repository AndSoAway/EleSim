#!/usr/bin/python
#-*- coding:utf-8 -*-

import os, codecs, sys

def fetch_data(flnms):
	data = {}
	res = {}
	prvns = []
	for flnm in flnms:
		flnm_parts = flnm.split('_')
		mthd = flnm_parts[0]
		data[mthd] = {}
		#mthds.append(mthd)
		fl = codecs.open(flnm, 'r', 'GB2312')
		for line in fl:
			line = line[:line.find(os.linesep)]
			line_parts = line.split(',')
			pro = line_parts[0]
			#print(pro)
			if pro not in data[mthd]:
				data[mthd][pro] = []
			if pro not in prvns:
				prvns.append(pro)
			data[mthd][pro].append(line_parts[1])
		fl.close()
	for prvn in prvns:
		if prvn not in res:
			res[prvn] = {}
		#print(prvn + "," + str(res[prvn]))
		for mthd in data:
			res[prvn][mthd] = data[mthd][prvn]
	return res

def jaccard(data):
	res = codecs.open('Jaccard.csv', 'w', 'utf-8')
	for prvn in data:
		DTW = data[prvn]['DTW']
		if prvn == 'Anhui':
			print(str(data[prvn]['DTW']))
		for mthd in data[prvn]:
			if mthd == 'DTW':
				continue
			array = data[prvn][mthd]
			intersect = []
			union = []
			for ele in array[:10]:
				union.append(ele)
				if ele in DTW[:10]:
					intersect.append(ele)
			for ele in DTW[:10]:
				if ele not in union:
					union.append(ele)
			int_cnt = len(intersect)
			unn_cnt = len(union)
			jaccard = float(int_cnt) / float(unn_cnt)
			res.write(prvn + ',' + mthd + ',' + str(jaccard) + ',' + str(int_cnt) + ',' + str(unn_cnt) + ',' + os.linesep)
	res.close()

if __name__ == "__main__":
	flnms = ['DTW_Res.csv', 'EDR_Res.csv', 'LCSS_Res.csv', 'res_file.csv']
	data = fetch_data(flnms)
	jaccard(data)