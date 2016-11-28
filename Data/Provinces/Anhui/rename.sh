#!/bin/sh
# Select*.txt Anhui-Select*.txt
for file in Select*
do
 new=${file/Select/Anhui-Select}
 mv $file $new
done
