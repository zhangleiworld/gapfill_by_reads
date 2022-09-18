#!/usr/bin/python
## Author: Lei Zhang (zhangleo1116@163.com)
import sys
import os
import re

f1=open(sys.argv[1]) ## paf 
length=int(sys.argv[2]) ## up and down-stream
f2=open(sys.argv[1]+'.gtLen','w')

## match paf 
for line1 in f1:
	list1=line1.strip().split()
	if len(list1) > 11:
		start=int(list1[2])
		end=int(list1[3])
		if (start < length) and (end > length):
			if (int(list1[8])-int(list1[7])) - (end-start) >= -100:
				f2.write(line1)
f1.close()
f2.close()

## select paf 
os.system('sort -k1,1 -k11,11nr {0}.gtLen > {0}.gtLen.sort'.format(sys.argv[1]))
f3=open(sys.argv[1]+'.gtLen.sort')
f4=open(sys.argv[1]+'.gtLen.sort.select','w') ## final results

flag=1
for line3 in f3:
	list3=line3.strip().split()
	if flag == 1:
		f4.write(line3)
		ID=list3[0]
		flag += 1
	else:
		IDnew=list3[0]
		if ID == IDnew:
			pass
		else:
			f4.write(line3)
			ID=IDnew
f3.close()
f4.close()

