#/usr/bin/python
#-*- coding:utf-8 -*-

import os

def crossX(a, b, c, d):
	denominator = b - a + c - d
	x = (c - a) / denominator
	return x

def crossY(a, b, c, d):
	denominator = b - a + c - d
	y = -((d - c) * a - (b - a) * c) / denominator
	return y

def lineCross(l1begin, l1end, l2begin, l2end):
	if ((l1begin < l2begin and l1end > l2end) or (l1begin > l2begin and l1end < l2end)):
		return True
	return False

def area(line1, line2):
	v_len = min(len(line1), len(line2))
	res = 0
	for i in range(v_len - 1):
		l1begin = line1[i]
		l1end = line1[i + 1]
		l2begin = line2[i]
		l2end = line2[i + 1]
		cur_area = 0
		if (lineCross(l1begin, l1end, l2begin, l2end) == True):
			inter_x = crossX(l1begin, l1end, l2begin, l2end)
			d1 = inter_x
			d2 = 1 - inter_x
			cur_area = (d1 * abs(l1begin - l2begin) + d2 * abs(l1end - l2end)) / 2
		else:
			cur_area = (abs(l1begin - l2begin) + abs(l1end - l2end)) / 2
		res = res + cur_area
		#print("cur_area: " + str(cur_area) + ", res: " + str(res))
	return res

def process(flnm1, flnm2):
	fl1 = codecs.open(flnm1, 'r', 'utf-8')
	fl2 = codecs.open(flnm2, 'r', 'utf-8')
	

if __name__ == "__main__":
	flnm1 = "Data/Provinces/Anhui/sum-安徽.csv"
	flnm2 = "Data/Provinces/Anhui/安徽省工业增加值增长速度.csv"