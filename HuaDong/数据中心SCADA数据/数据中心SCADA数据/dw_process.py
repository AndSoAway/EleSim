#!/usr/bin/python
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def printFields(file_name):
    ori_file = codecs.open(file_name, 'r', 'gbk')
    fields_names = ori_file.readline()
    i = 0
    for line in ori_file:
        loc = line[1:line.find(',') -1]
        print(loc)
        i += 1
        if i > 10:
            return

def cutFiles(file_name):
    ori_file = codecs.open(file_name, 'r', 'gbk')
    field_names = ori_file.readline()
    record_dict = {}
    i = 0
    for line in ori_file:
#        first_comma = line.index(',')
        loc = line[:line.find(',')][1:-1]
        if loc not in record_dict.keys():
            record_dict[loc] = []
        record_dict[loc].append(line)
    for loc in record_dict.keys():
        records = record_dict[loc]
        loc_file = open(loc + '_' + file_name, 'w')
        loc_file.write(field_names)
        for record in records:
            loc_file.write(record)
        loc_file.close()

if __name__ == "__main__":
    dw = "DW_R_MIN_DW.csv"
    ace = "DW_R_SEC_ACE.csv"
    cutFiles(dw)
    cutFiles(ace)
