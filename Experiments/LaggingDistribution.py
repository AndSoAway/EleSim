#!/usr/bin/python

import codecs, os, sys

def getDistribution(flnms):
	prvns = ['Anhui', 'Fujian', 'Jiangsu', 'Shanghai', 'Zhejiang']
	data = {}
	mthds = ['Area', 'DTW', 'EDR', 'LCSS']
	for prvn in prvns:
		data[prvn] = {}
		for mthd in mthds:
			data[prvn][mthd] = {} 
			for x in range(12):
				data[prvn][mthd][x + 1] = 0
				data[prvn][mthd][-(x + 1)] = 0
			data[prvn][mthd][0] = 0

	for flnm in flnms:
		print(flnm)
		flnm_parts = flnm.split('_')
		mthd = flnm_parts[0]
		fl = codecs.open(flnm, 'r', 'GBK')
		for line in fl:
			pos = line.find(os.linesep)
			line = line if pos == -1 else line[:line.find(os.linesep)]
			print(line)
			line_parts = line.split(',')
			print(line_parts)
			prvn = line_parts[0]

			print(prvn + mthd + line_parts[4])
			month = float(line_parts[4])
			data[prvn][mthd][month] = 1 + data[prvn][mthd][month]
		fl.close()

	month = range(-12,13,1)
	for prvn in prvns:
		res_flnm = prvn + "_lagging_dis.csv"
		fl = codecs.open(res_flnm, 'w', 'utf-8')
		prvn_data = data[prvn]
		for x in month:
			line = str(x)
			for mthd in mthds:
				line = line + ' ' + str(data[prvn][mthd][x])
			line = line + os.linesep
			fl.write(line)


if __name__ == "__main__":
	flnms = ['Area_Sim.csv', 'DTW_Res.csv', 'EDR_Res.csv', 'LCSS_Res.csv']
	getDistribution(flnms)